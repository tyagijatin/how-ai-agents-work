# A coding agent in 100 lines

The code from **Agent Harnesses Explained #2: The Agent Loop in 100 Lines**. `agent.py` is the whole agent:
three tools, the loop, a stop rule and a permission prompt, on the Anthropic Messages API.

```bash
pip install -r requirements.txt          # the official `anthropic` SDK
export ANTHROPIC_API_KEY=...             # or `ant auth login`
cd some/project
python path/to/agent.py "One of the tests is failing. Find the bug and fix it, then run the tests to confirm."
```

It asks before every edit and command. `--yes` skips the prompts: only use it in a throwaway copy of a project.

| Part | What it does |
|---|---|
| `TOOLS` | Three tool descriptions the model reads: `read_file`, `edit_file`, `run_command` |
| `read_file` / `edit_file` / `run_command` | The code that actually runs when the model asks |
| `allowed` | Control: asks before anything that changes files or runs code |
| `run_tool` | Runs one tool call; errors go back to the model as results instead of crashing |
| `agent` | The loop: call the model, run the tools it asked for, append everything, repeat until it stops asking |

What it deliberately leaves out, and the episode that adds it: context management and compaction (5, 8), memory
(7), subagents and skills (9, 10), hooks (11), a real sandbox (12). Run it only in a directory you're happy for it to change.

- **Model:** `claude-opus-5-5`, with the API's default adaptive thinking and effort.
- **Refusals:** a `refusal` stop reason ends the loop. For production, the API also offers server-side
  fallbacks for refusals (a beta parameter); they're left out here to keep the loop readable.
- **`trace_log.py`:** only used for the video (`--trace trace.jsonl`). It records the session in the same shape as
  Claude Code's `--output-format stream-json`.
