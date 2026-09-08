## Why

The project has no consistent language guard. Code, README, comments, commit messages, and docs produced or edited by AI assistants can end up in Spanish or mixed languages. The team wants every change -- to code, README, or any project file -- written in English, so the repository stays consistent and professional for any audience.

## What Changes

- Add a reusable opencode skill named `enforce-english` that instructs the AI to write everything in English.
- Add an `AGENTS.md` guard at the repo root stating the global "English only" rule for all AI-generated modifications.
- The guard applies to: source code (strings, identifiers, comments, docstrings), README, documentation, templates, tests, commit messages, and any other project file.
- The user-facing project files (e.g., templates) must remain in English too; this is an enforcement rule, not a migration of existing historical content.

## Capabilities

### New Capabilities

- `enforce-english`: a guard rule, exposed as an opencode skill (`enforce-english`) and a root-level `AGENTS.md` entry, that requires all code, documentation, README, comments, and any project file changes to be written in English.

### Modified Capabilities

<!-- No existing specs to modify. -->

## Impact

- New files: `.opencode/skills/enforce-english/SKILL.md` and `AGENTS.md`.
- No changes to runtime code, APIs, dependencies, or database schema.
- Affected systems: AI-assisted workflows in opencode; repository conventions and contribution guidelines.