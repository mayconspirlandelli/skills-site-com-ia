# Manual review of the `impeccable` skill

- **Repository:** https://github.com/pbakaus/impeccable (≈99k stars, Apache-2.0)
- **Installed path:** `.claude/skills/impeccable` (the repository ships one variant per tool; this is the Claude Code one)
- **Reviewed commit:** `e89e3ad` (version 4.8.0)
- **Date:** 2026-11-02
- **Automatic verdict:** ⛔ BLOCK · **User decision:** ✅ include in full, as required, accepting the binary

## What the skill does

Interface design guides (critique, audit, polish, typography, color, layout, motion, accessibility, design system) and a command-line engine with a design-issue detector, a "live" in-browser variants mode and post-edit hooks.

## Findings

| Item | Assessment |
|------|------------|
| 8 CRITICAL alerts in `reference/*.md` | False positives: phrases like "don't tell the user they need to invoke `craft`", "don't show the findings before the synthesis", "don't disable browser security". |
| "Obfuscated" `modern-screenshot.umd.js` | Minified third-party library (in-browser screenshots), not malicious obfuscation. |
| Network in JS scripts | Only `http://localhost` (the skill's own local server). No telemetry. |
| **Engine binary** | The `scripts/impeccable` launcher downloads a compiled (Go) binary for the OS from the GitHub releases page and runs it, caching it. There is an `engine-checksums.txt` in the commit (the checksum pins the binary), but **a binary cannot be audited by reading**. |
| **Hooks** | The `hooks` command writes post-edit hooks to `.claude/settings.local.json` (or `~/.claude/settings.json`). It asks for consent first. |
| **Live mode** | Injects a script into the page open in the browser and tells the AI to follow the `_instructions` field returned by the tool itself. Restricted to local servers. |

## Conditions of use in the project

1. Always install the fixed commit `e89e3ad` (`setup-skills.sh` does this), which also pins the binary's version and checksum.
2. Exception recorded in `auditorias/excecoes.txt`; the script still asks for confirmation on install.
3. Enable the hooks only when the user asks (the command asks for consent).
4. Updating to another commit requires a new review.
