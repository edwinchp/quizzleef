---
name: enforce-english
description: Enforce English-only project content. Use on EVERY task and EVERY change to code, README, documentation, templates, tests, comments, commit messages, or any other project file. Applies as a guard: all new and edited repository content must be written in English.
license: MIT
compatibility: Works with any opencode project.
metadata:
  author: quizzleef
  version: "1.0"
---

# Enforce English

Every project change you make MUST be written in English. This is a guard rule for the entire repository.

## Scope

This rule applies to **project files and commit messages**:

- Source code: strings, user-facing text, identifiers, variable/function names, comments, docstrings
- README, documentation, and any markdown or text files
- HTML/Jinja/Django templates and any user-visible labels
- Tests and test fixtures
- Configuration examples and sample data written into the repo
- Commit messages: always written in English

## Out of Scope

- **Chat replies**: You may answer the user in any language they use. This rule governs repository artifacts only.
- **Pre-existing content**: Do NOT migrate or rewrite existing non-English content unless the user explicitly asks. Only new and edited content must be English.
- **External quotes/citations**: Keep verbatim quoted content as-is.

## Rules

1. When creating or editing ANY file, write all content in English.
2. When a task mixes languages in the UI copy, translate the copy to English before writing it to a file.
3. Never emit TODO/FIXME comments or log messages in a language other than English.
4. Use idiomatic English naming for code identifiers (no Spanish/Castilian names) unless the project explicitly uses a term as data.
5. Before finishing any change, scan the files you wrote/edited and correct any non-English fragments you introduced.

## Self-check

Before reporting a task as complete, verify that:

- [ ] Every file you created or edited reads entirely in English
- [ ] Comments and docstrings are in English
- [ ] Templates/UI labels are in English
- [ ] Commit messages you generated are in English