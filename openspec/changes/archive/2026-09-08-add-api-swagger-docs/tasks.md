## 1. Add drf-spectacular dependency

- [x] 1.1 Add `drf-spectacular` to `requirements.txt`.

## 2. Configure drf-spectacular in settings

- [x] 2.1 Add `drf_spectacular` to `INSTALLED_APPS` in `quizzleef/settings.py`.
- [x] 2.2 Add `REST_FRAMEWORK.DEFAULT_SCHEMA_CLASS = 'drf_spectacular.openapi.AutoSchema'` in `quizzleef/settings.py`.
- [x] 2.3 Add `SPECTACULAR_SETTINGS` with title "Quizzleef API" and a version in `quizzleef/settings.py`.

## 3. Wire schema and Swagger UI URLs (debug-only)

- [x] 3.1 Add `SpectacularAPIView` at path `api/schema/` in `quizzleef/urls.py`.
- [x] 3.2 Add `SpectacularSwaggerView` at path `api/docs/` in `quizzleef/urls.py`.
- [x] 3.3 Wrap both doc routes in `if settings.DEBUG:` so they are not registered in production.

## 4. Annotate API views with @extend_schema

- [x] 4.1 Document `get_question_by_id`: `pk` path parameter, QuestionSerializer response, 404 error.
- [x] 4.2 Document `get_random_question`: `category`, `difficulty`, `count` query parameters, 200/400/404/500 responses.
- [x] 4.3 Document `create_question`: multipart/form-data and JSON request body, 201/400/500 responses.
- [x] 4.4 Document `create_questions_bulk`: list or `{items:[...]}` request body, 201/207/400 responses.

## 5. Add the api-docs maintenance skill

- [x] 5.1 Create `.opencode/skills/api-docs/SKILL.md` with rules requiring `@extend_schema` updates and `spectacular --validate` on any API change.

## 6. Verify

- [x] 6.1 Run `python manage.py spectacular --file /tmp/schema.yml --validate` and confirm the schema is valid.
- [x] 6.2 Confirm `GET /api/schema/` and `GET /api/docs/` respond when `DEBUG=True`.
- [x] 6.3 Confirm the doc routes are absent (404) when `DEBUG=False`.