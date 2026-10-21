# Demo: the 100-line agent fixes the failing test

The same invoice repo, prompt and model (`claude-opus-5-5`) as episode 1's Claude Code session
(`../../01-what-is-a-harness/demo`), run with `agent.py --yes --trace` in a throwaway copy on 21 Oct 2026.

- `trace.jsonl`: the session, recorded by `trace_log.py` in Claude Code's stream-json shape.
- `terminal.log`: what the agent printed.
- `fix.diff`: the change it made. All 3 tests pass afterwards.

| | agent.py (93 lines) | Claude Code (episode 1) |
|---|---|---|
| Tools available | 3 | 27 |
| Model calls | 5 | 6 |
| Tool calls | 5 | 9 |
| Tokens the model read on call 1 | 654 | 16,143 |
| Time | 16.9 s | 23.0 s |
| Cost (list price) | $0.043 | $0.108 |

One small task, one run each, so this isn't a benchmark. Claude Code's extra 15,000 tokens of instructions and
tools are there for the many jobs this toy agent can't do.
