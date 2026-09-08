## 1. Create the enforce-english skill

- [x] 1.1 Create `.opencode/skills/enforce-english/SKILL.md` with frontmatter (`name: enforce-english`, description that triggers on any project edit) and English-only rules for code, README, docs, templates, tests, comments, and commit messages.
- [x] 1.2 State explicitly that the rule covers project files only, not chat replies, and that pre-existing non-English content is not migrated.

## 2. Add the global AGENTS.md guard

- [x] 2.1 Create `AGENTS.md` at the repo root with a clear global "All project changes must be written in English" instruction.
- [x] 2.2 Reference the `enforce-english` skill in `AGENTS.md` so assistants load/apply it.

## 3. Verify

- [x] 3.1 Confirm the skill file is discoverable at `.opencode/skills/enforce-english/SKILL.md` with valid frontmatter.
- [x] 3.2 Confirm `AGENTS.md` exists at the repo root and states the English-only rule.
- [x] 3.3 (Optional) Ask opencode to restart and confirm the `/opsx` style command surface or skill listing includes `enforce-english` without errors.