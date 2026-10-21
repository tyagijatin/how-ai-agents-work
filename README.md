# How AI agents actually work: code

Code, demo repos and recorded agent sessions from the YouTube channel
[@im_jatintyagi](https://www.youtube.com/@im_jatintyagi): AI agents explained by an engineer who builds them.

## Agent Harnesses Explained

| # | Episode | What's here |
|---|---|---|
| 1 | What Is an Agent Harness? Same AI Model, Very Different Agent | [`demo/`](agent-harnesses/01-what-is-a-harness/demo): the invoice repo with one failing test, and the real Claude Code session that fixed it (`trace.jsonl`, stream-json) |
| 2 | The Agent Loop in 100 Lines | [`agent.py`](agent-harnesses/02-agent-loop-100-lines/agent.py): a working coding agent in under 100 lines of Python, on the Anthropic API |

More episodes are added as they're published.

## Running the code

Each episode folder has its own README. The agents need an Anthropic API key (`ANTHROPIC_API_KEY`) and can
edit files and run commands, so run them only in a throwaway copy of a project.

## License

MIT, see [LICENSE](LICENSE). Paper figures and quotes shown in the videos belong to their authors.
