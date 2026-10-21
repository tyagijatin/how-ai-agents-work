"""A coding agent in 100 lines (Agent Harnesses Explained #2). Usage: python agent.py "task" [--yes]"""
import argparse
import json
import pathlib
import subprocess

import anthropic

MODEL = "claude-opus-5-5"
SYSTEM = (
    "You are a coding agent working in the current directory. Use the tools to look at files, "
    "run commands and make edits. Check your work by running the tests. Finish with a short summary."
)
MAX_TURNS = 20  # stop rule: never loop forever
MAX_OUTPUT = 10_000  # characters of tool output the model gets to see

# Tools are just descriptions. The model reads these; it never runs anything itself.
TOOLS = [
    {"name": "read_file", "description": "Read a text file. Returns its contents with line numbers.",
     "input_schema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
    {"name": "edit_file",
     "description": "Replace text in a file. `old` must appear exactly once, so include enough surrounding text.",
     "input_schema": {"type": "object", "properties": {
         "path": {"type": "string"}, "old": {"type": "string"}, "new": {"type": "string"}},
         "required": ["path", "old", "new"]}},
    {"name": "run_command", "description": "Run a shell command. Returns the exit code and its output.",
     "input_schema": {"type": "object", "properties": {"command": {"type": "string"}}, "required": ["command"]}},
]

def read_file(path):
    lines = pathlib.Path(path).read_text().splitlines()
    return "\n".join(f"{n}\t{line}" for n, line in enumerate(lines, 1))

def edit_file(path, old, new):
    file = pathlib.Path(path)
    text = file.read_text()
    if text.count(old) != 1:
        raise ValueError(f"`old` appears {text.count(old)} times in {path}; it must appear exactly once")
    file.write_text(text.replace(old, new))
    return f"Edited {path}."

def run_command(command):
    done = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60)
    return f"exit code {done.returncode}\n{done.stdout}{done.stderr}"

HANDLERS = {"read_file": read_file, "edit_file": edit_file, "run_command": run_command}

def allowed(name, args, yes):
    """Control: ask before anything that changes files or runs code."""
    if yes or name == "read_file":
        return True
    return input(f"Allow {name} {json.dumps(args)}? [y/N] ").strip().lower() == "y"

def run_tool(call, yes):
    print(f"> {call.name} {json.dumps(call.input)[:120]}")
    if not allowed(call.name, call.input, yes):
        return {"type": "tool_result", "tool_use_id": call.id, "content": "The user declined.", "is_error": True}
    try:
        output = HANDLERS[call.name](**call.input)
        return {"type": "tool_result", "tool_use_id": call.id, "content": output[:MAX_OUTPUT]}
    except Exception as error:  # errors go back to the model as observations, so it can recover
        return {"type": "tool_result", "tool_use_id": call.id, "content": f"Error: {error}", "is_error": True}

def agent(task, yes=False, log=lambda kind, data: None):
    client = anthropic.Anthropic()
    messages = [{"role": "user", "content": task}]  # the model remembers nothing: we resend this every call
    for _ in range(MAX_TURNS):
        response = client.messages.create(
            model=MODEL, max_tokens=16000, system=SYSTEM, tools=TOOLS, messages=messages)
        log("assistant", response)
        messages.append({"role": "assistant", "content": response.content})  # keep everything, append-only
        for block in response.content:
            if block.type == "text":
                print(block.text)
        if response.stop_reason != "tool_use":  # end_turn: done. max_tokens or refusal: stop too
            return response.stop_reason
        results = [run_tool(call, yes) for call in response.content if call.type == "tool_use"]
        log("user", results)
        messages.append({"role": "user", "content": results})  # every result in one message
    return "max_turns"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A coding agent in 100 lines.")
    parser.add_argument("task")
    parser.add_argument("--yes", action="store_true", help="don't ask before edits and commands")
    parser.add_argument("--trace", help="write a stream-json style trace (see trace_log.py)")
    args = parser.parse_args()
    if args.trace:
        from trace_log import TraceLog
        with TraceLog(args.trace, MODEL, TOOLS) as trace:
            print("stopped:", agent(args.task, args.yes, trace.log))
    else:
        print("stopped:", agent(args.task, args.yes))
