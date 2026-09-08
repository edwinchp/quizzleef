## Why

The Quizzleef project exposes a Django REST Framework API (question retrieval, random question, create single/bulk questions) but has no visual documentation. Consumers cannot easily discover what endpoints exist, what parameters they take, or what responses to expect. The API is expected to grow, so the docs should stay in sync with the code with minimal manual effort.

## What Changes

- Add `drf-spectacular` to generate an OpenAPI 3 schema automatically from the DRF code.
- Publish the schema at `GET /api/schema/` and an interactive Swagger UI at `GET /api/docs/`.
- Make the docs endpoints available only when `DEBUG` is enabled, to avoid exposing API surface in production.
- Add `@extend_schema` decorators to the four existing API views so the generated schema is fully documented (parameters, request/response bodies, error codes).
- Add an opencode skill `api-docs` that enforces keeping the API documentation in sync as endpoints change.

No behavior changes to the existing endpoints or responses.

## Capabilities

### New Capabilities

- `api-docs`: automatic OpenAPI 3 schema generation and interactive Swagger UI, available during debug, with per-endpoint documentation annotations and a maintenance skill to keep it current.

### Modified Capabilities

<!-- No existing specs to modify. -->

## Impact

- New dependency: `drf-spectacular`.
- Modified files: `requirements.txt`, `quizzleef/settings.py`, `quizzleef/urls.py`, `questions/api_views.py`.
- New files: `.opencode/skills/api-docs/SKILL.md`.
- No database schema changes, no runtime endpoint behavior changes.