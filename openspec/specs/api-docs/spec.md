# Capability: api-docs

## Purpose

Provide auto-generated OpenAPI 3 and interactive Swagger UI documentation for the project's DRF API, available only in debug mode, and keep it current as endpoints evolve.

## Requirements

### Requirement: OpenAPI schema generation

The project SHALL generate an OpenAPI 3 schema automatically from the DRF code, serving it at `GET /api/schema/`.

#### Scenario: Schema endpoint returns valid OpenAPI

- **WHEN** a client requests `GET /api/schema/` with DEBUG enabled
- **THEN** the server returns a valid OpenAPI 3 document describing all API endpoints

#### Scenario: Schema reflects current endpoints

- **WHEN** an API endpoint is added or removed from the codebase
- **THEN** the generated schema at `GET /api/schema/` reflects the change without manual schema editing

### Requirement: Interactive Swagger UI

The project SHALL expose an interactive Swagger UI at `GET /api/docs/` that renders the generated OpenAPI schema.

#### Scenario: Swagger UI renders endpoints

- **WHEN** a client navigates to `GET /api/docs/` with DEBUG enabled
- **THEN** the Swagger UI loads and lists all documented endpoints with their parameters and responses

### Requirement: Docs only in debug mode

The API documentation endpoints (`/api/schema/` and `/api/docs/`) SHALL be available only when Django `DEBUG` is enabled.

#### Scenario: Docs visible with DEBUG on

- **WHEN** `settings.DEBUG` is `True`
- **THEN** the docs endpoints are registered and accessible

#### Scenario: Docs hidden with DEBUG off

- **WHEN** `settings.DEBUG` is `False`
- **THEN** the docs endpoints are not registered and return 404

### Requirement: Per-endpoint documentation

All API views SHALL be annotated with `@extend_schema` describing their parameters, request body, and responses.

#### Scenario: GET question by id is annotated

- **WHEN** docs are generated
- **THEN** the `GET /api/question/{pk}` endpoint documents the `pk` path parameter and the question response schema

#### Scenario: Random question endpoint is annotated

- **WHEN** docs are generated
- **THEN** the `GET /api/random-question/` endpoint documents the `category`, `difficulty`, and `count` query parameters and its response schemas

#### Scenario: Create question endpoint is annotated

- **WHEN** docs are generated
- **THEN** the `POST /api/questions/` endpoint documents its multipart/form-data and JSON request body and the created question response

#### Scenario: Bulk create endpoint is annotated

- **WHEN** docs are generated
- **THEN** the `POST /api/questions/bulk/` endpoint documents its list/`items` request body and its success/partial-success responses

### Requirement: Docs maintenance skill

The project SHALL provide an opencode skill named `api-docs` that instructs assistants to update `@extend_schema` annotations and validate the schema whenever API code changes.

#### Scenario: Skill is available

- **WHEN** opencode loads the project's skills
- **THEN** a skill named `api-docs` is available with rules for keeping API docs current