# Demo: Claude Code fixes a failing test

- `repo/`: the tiny invoice calculator, as the agent found it. `test_discount_code` fails (`117.88 != 106.2`) because
  `discounts.lookup()` returns a fraction and `invoice_total()` divides it by 100 again.
- `trace.jsonl`: the session as `stream-json`, replayed by `TraceReplay` in the video.
- `fix.diff`: the change the agent made.

Captured on 19 Oct 2026 (Claude Code 2.1.303, `claude-opus-5-5`) on a copy of `repo/` in `/tmp/ah01-demo`, after
`git init` and one commit:

```bash
claude -p "One of the tests is failing. Find the bug and fix it, then run the tests to confirm." \
  --output-format stream-json --verbose --safe-mode --strict-mcp-config \
  --permission-mode acceptEdits --allowedTools "Bash(python3 -m unittest*)" --permission-prompts none \
  --no-session-persistence > trace.jsonl
```

`--safe-mode` keeps personal CLAUDE.md files, skills and MCP servers out of the session, so the trace shows stock Claude
Code. Before committing, the trace was trimmed: the `rate_limit_event` and `ui_invalidate` events were removed, and the
`init` event was cut down to cwd, session ID, tools, MCP servers, model, permission mode, version, agents and skills.
Everything else is unchanged.

Re-running gives a different (but similar) session; the video uses this one.
