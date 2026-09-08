---
name: api-docs
description: Keep the OpenAPI/Swagger documentation of this project's API in sync with the code. Use on ANY change that touches or adds API views, serializers, URL patterns, or response/error handling. Requires every API modification to include an @extend_schema update and a schema validation run.
license: MIT
compatibility: Requires drf-spectacular and the drf_spectacular Django management command.
metadata:
  author: quizzleef
  version: "1.0"
---

# API Docs Guard

The Quizzleef API is documented through `drf-spectacular`, which auto-generates an OpenAPI 3 schema from the code and serves it at `/api/schema/` with an interactive Swagger UI at `/api/docs/` (both only when `DEBUG=True`).

Auto-generation keeps the schema in sync structurally, but the **quality** of the docs depends on hand-written `@extend_schema` annotations. This skill guards that they are kept current whenever the API changes.

## Rules

1. **Every API change must touch `@extend_schema`**. When you add, modify, or remove an endpoint in `questions/api_views.py` (or another API view), also add or update its `@extend_schema` decorator.

2. **Document the full contract** in `@extend_schema`:
   - `description` of what the endpoint does.
   - `parameters` via `OpenApiParameter` for query/path/header params (name, type, location, required, enum when known).
   - `request` for POST/PUT/PATCH (serializer, or a dict of content types; `inline_serializer` for nested/flexible bodies).
   - `responses` mapping every status code the view can return (200/201/207/400/404/500, etc.) using `OpenApiResponse` or a serializer.

3. **Path parameters are auto-derived** from the URL pattern. Do NOT add explicit path parameters for int converters unless customizing type/description (Django coerce: `{pk}` renders as `{id}`). Adding a duplicate path parameter produces a broken schema.

4. **When serializers change** (fields added/removed/renamed in `quizzleef/serializers.py` or the models they map), the schema picks it up automatically — no manual step needed beyond verification.

5. **Validate after every API change**:

   ```bash
   python manage.py spectacular --file /tmp/schema.yml --validate
   ```

   Fix any warnings/errors before finishing. A 0-error result is required.

6. **Add regression coverage** for new endpoints if the project's test suite covers API behavior.

## Self-check

Before reporting any API-related task complete, verify that:

- [ ] Every touched/changed endpoint has a complete `@extend_schema`
- [ ] New query/path/header params are documented via `OpenApiParameter`
- [ ] Request body is documented (serializer or inline_serializer)
- [ ] All possible response status codes appear in `responses`
- [ ] `python manage.py spectacular --file /tmp/schema.yml --validate` reports 0 errors
- [ ] No duplicate path parameters were introduced