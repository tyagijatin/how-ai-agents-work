"""Records an agent.py session in the same shape as Claude Code's `--output-format stream-json`.

Kept out of agent.py so the agent itself stays at 100 lines. Used only for the video's trace replay.
"""
import json
import os
import time

# Claude Opus 5.5 list prices, USD per million tokens (input, output, cache read, cache write).
PRICES = {"claude-opus-5-5": (4.00, 20.00, 0.20, 5.00)}


class TraceLog:
    def __init__(self, path, model, tools):
        self.path, self.model, self.tools = path, model, tools
        self.usage = {"input_tokens": 0, "output_tokens": 0, "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0}

    def __enter__(self):
        self.file = open(self.path, "w")
        self.start = time.time()
        self.write({"type": "system", "subtype": "init", "cwd": os.getcwd(), "model": self.model,
                    "tools": [t["name"] for t in self.tools], "claude_code_version": "agent.py (100 lines)"})
        return self

    def write(self, event):
        self.file.write(json.dumps(event, ensure_ascii=False) + "\n")

    def log(self, kind, data):
        if kind == "assistant":
            message = data.model_dump(mode="json", exclude_none=True)
            for key in self.usage:
                message["usage"][key] = message["usage"].get(key) or 0
                self.usage[key] += message["usage"][key]
            self.write({"type": "assistant", "message": message})
        else:
            self.write({"type": "user", "message": {"role": "user", "content": data}})

    def __exit__(self, *exc):
        p_in, p_out, p_read, p_write = PRICES.get(self.model, (0, 0, 0, 0))
        u = self.usage
        cost = (u["input_tokens"] * p_in + u["output_tokens"] * p_out + u["cache_read_input_tokens"] * p_read
                + u["cache_creation_input_tokens"] * p_write) / 1e6
        self.write({"type": "result", "duration_ms": round((time.time() - self.start) * 1000),
                    "total_cost_usd": round(cost, 6), "usage": u})
        self.file.close()
