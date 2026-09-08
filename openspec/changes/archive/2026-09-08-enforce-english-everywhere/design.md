## Context

The repository (a Django "Quizzleef" question manager) relies on an AI coding assistant (opencode) that edits code, documentation, README, templates, tests, and generates commit messages. There is currently no rule specifying the language for generated content, so output can drift between Spanish and English or become mixed. The goal is a lightweight, repo-level guard that keeps all new/edited content in English without requiring runtime changes.

Constraints:
- opencode loads skills from `.opencode/skills/<name>/SKILL.md`.
- opencode reads `AGENTS.md` at the repo root as global project instructions for assistants.
- The existing OpenSpec skills live under `.opencode/skills/`; new skills follow the same frontmatter format.
- This is a convention/guard change only: no Python/Django code or schema changes.

## Goals / Non-Goals

**Goals:**
- Provide a reusable opencode skill, `enforce-english`, that instructs the assistant to write all code and files in English.
- Provide a global `AGENTS.md` rule so the English-only behavior applies even when the skill is not explicitly surfaced.
- Cover code, README, docs, templates, tests, comments/docstrings, and commit messages.

**Non-Goals:**
- Migrating or rewriting pre-existing non-English content.
- Enforcing English on user chat responses (only project artifacts).
- Building CI/lint checks for language enforcement.

## Decisions

**Decision 1: Create both a skill and an AGENTS.md guard.**
- *Rationale*: The skill (`enforce-english`) is portable, self-describing, and auto-loaded by opencode; `AGENTS.md` is the universal convention that any agent reads at the repo root. Together they maximize enforcement coverage.
- *Alternatives considered*: Skill only (weaker guarantee because skills may not always match intent) vs. AGENTS.md only (no reusable/portable name). Chose both.

**Decision 2: Name the skill `enforce-english` and place it at `.opencode/skills/enforce-english/SKILL.md`.**
- *Rationale*: Matches opencode's skill discovery convention and parallels the existing OpenSpec skills. The frontmatter `description` is written to trigger whenever any project file edit is requested.
- *Alternatives considered*: A single global config instruction in `opencode.json` (less discoverable, harder to attach a reusable prompt).

**Decision 3: English applies to project artifacts, not to chat replies.**
- *Rationale*: The user communicates in Spanish; only repository content must be English. This is stated explicitly in the skill to avoid over-reaching.
- *Alternatives considered*: Enforcing English in all AI output (rejected: hurts usability for a Spanish-speaking operator).

**Decision 4: Do not migrate existing content.**
- *Rationale*: Migration would touch unrelated lines and create noise; the guard governs new and edited content only.
- *Alternatives considered*: Full-repo re-language pass (rejected as out of scope, risky).

## Risks / Trade-offs

- [Skill may not fire automatically on every edit] → Mitigation: also ship the `AGENTS.md` rule, which is read unconditionally by opencode.
- [Over-reach into chat output] → Mitigation: explicit non-goal in the skill limiting enforcement to project files.
- [Existing non-English content lingers] → Mitigation: documented as a non-goal; welcome to a future dedicated migration change.