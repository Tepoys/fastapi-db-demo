# How to run

1. Make sure Postgresql is running
2. Create venv `uv venv`
3. Activate venv `source ./.venv/bin/activate`
4. Sync dependencies `uv sync`
5. Create db named `db.postgresql` in postgres
6. Start server `uv run uvicorn main:app --reload`
