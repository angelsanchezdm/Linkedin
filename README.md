# LinkedIn

Project-local install of [linkedin-agent-skill](https://github.com/Jakeschincariol/linkedin-agent-skill)
(v1.0, commit add2c23, MIT - see `LICENSE.linkedin-agent-skill`).

Skills live in `.claude/skills/li-*` and load automatically when Claude Code runs in this repo:
`/li-post`, `/li-comment`, `/li-reply`, `/li-profile`, `/li-plan`, `/li-human`,
`/li-carousel`, `/li-repurpose`, `/li-dm`, `/li-inbox`, `/li-audit`.

Before first use, fill in `templates/voice.md` and copy it to `~/.claude/linkedin/voice.md`
(or paste three of your past posts into `/li-post` and it will write that file for you).
