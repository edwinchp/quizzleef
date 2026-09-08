# Capability: enforce-english

## Purpose

Ensure all AI-generated project changes are written in English, and expose this rule to AI assistants through available mechanisms.

## Requirements

### Requirement: English-only project changes

All project changes made by the AI SHALL be written in English. This covers source code (strings, identifiers, comments, docstrings), README, documentation, templates, tests, commit messages, and any other project file. Existing content is not migrated; only new and edited content MUST be in English.

#### Scenario: AI edits source code

- **WHEN** the AI creates or modifies source code files
- **THEN** all strings, identifiers, comments, and docstrings are written in English

#### Scenario: AI edits README or documentation

- **WHEN** the AI creates or modifies README, docs, or any project documentation file
- **THEN** the content is written entirely in English

#### Scenario: AI writes a commit message

- **WHEN** the AI generates a commit message
- **THEN** the message is written in English

#### Scenario: Existing non-English content is preserved

- **WHEN** the AI encounters pre-existing non-English content that is not part of the current change
- **THEN** the AI leaves that historical content unchanged rather than migrating it

### Requirement: Guard is available to the assistant

The project SHALL expose the English-only rule to AI assistants through both an opencode skill named `enforce-english` and a root-level `AGENTS.md` file that states the rule globally.

#### Scenario: opencode loads the skill

- **WHEN** opencode loads the project's skills
- **THEN** a skill named `enforce-english` is available with the English-only rule applied

#### Scenario: Root-level AGENTS.md exists

- **WHEN** an AI assistant reads the repository root conventions
- **THEN** the `AGENTS.md` file states the global English-only rule for all project changes
