## Context

Quizzleef is a Django 5.1 + Django REST Framework project. Current API endpoints are function-based views in `questions/api_views.py` using `@api_view` and custom parsers (JSON + multipart/form-data). There is no API documentation today. The project runs in Docker with nginx proxying all paths to gunicorn/web, so any new URL under `/` is automatically reachable.

The repo already uses opencode skills under `.opencode/skills/` (including the `enforce-english` guard) and an OpenSpec workflow under `openspec/`.

Constraints:
- Docs must not change endpoint behavior.
- Docs endpoints must only be live in development (`DEBUG=True`).
- Must run inside Docker; nginx requires no changes for `/api/*`.

## Goals / Non-Goals

**Goals:**
- Auto-generated OpenAPI 3 schema from DRF code (stays in sync as endpoints grow).
- Interactive Swagger UI for consumers.
- Per-endpoint documentation through `@extend_schema`.
- A `api-docs` opencode skill to keep annotations updated on API changes.

**Non-Goals:**
- Adding authentication to the API endpoints themselves.
- Migrating to DRF class-based views (current function views stay).
- Building custom schema authoring/editing tooling.
- Restricting docs by users/roles (only `DEBUG` gating).

## Decisions

**Decision 1: Use `drf-spectacular` (not `drf-yasg`).**
- *Rationale*: `drf-spectacular` is the actively maintained standard that generates the OpenAPI 3 schema from DRF introspection and supports function views, custom parsers, and `@extend_schema`. It also ships a CLI validator (`spectacular --validate`).
- *Alternatives considered*: `drf-yasg` (Swagger 2.0, less maintained, heavier), hand-written `static/spec.yml` (manual drift). Chose `drf-spectacular`.

**Decision 2: Gate docs endpoints with `if settings.DEBUG`.**
- *Rationale*: The POST endpoints can create questions; hiding schema/UI in production avoids exposing API surface. Simple conditional in `urlpatterns` yields a clean 404 when `DEBUG=False`.
- *Alternatives considered*: Custom `permission_classes` on the schema/UI views (more moving parts), environment variable flag (extra config). Chose `DEBUG` gating.

**Decision 3: Keep function views and annotate with `@extend_schema`.**
- *Rationale*: Preserves the existing code style and avoids a rewrite; `@extend_schema` provides parameters, request, and response documentation for each endpoint (including the multipart create flow).
- *Alternatives considered*: Converting to class-based `APIView`/`ViewSet` (bigger refactor, out of scope). Chose function views + decorators.

**Decision 4: Expose Swagger UI only (no ReDoc).**
- *Rationale*: User requested Swagger UI only; one view keeps surface minimal. ReDoc can be added later trivially.
- *Alternatives considered*: Adding ReDoc too (rejected by user).

**Decision 5: Add `api-docs` skill as the no-drift mechanism.**
- *Rationale*: The schema auto-generates, but annotations are manual; a skill (mirroring `enforce-english`) instructs assistants to update `@extend_schema` and run `spectacular --validate` whenever API code changes.
- *Alternatives considered*: Relying only on auto-generation (loses descriptive docs), CI schema check (no CI currently). Chose the skill.

## Risks / Trade-offs

- [Multipart create endpoint may generate awkward schema] → Mitigation: document request as both JSON and multipart in `@extend_schema` (`request` description and `consumes`).
- [Bulk endpoint has flexible body (list or `{items:}`)] → Mitigation: describe both shapes via `@extend_schema` request examples; keep 201/207 responses documented.
- [Debug gating on by default (DEBUG=True in settings)] → Mitigation: acceptable for current dev-only usage; flag noted in the skill/design for future hardening.