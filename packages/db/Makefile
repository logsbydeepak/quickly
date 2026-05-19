init_db:
	uv run python -c "import main; main.init_db()"

drop_db:
	uv run python -c "import main; main.drop_db()"

sync_db:
	uv run python sync.py "$(SOURCE_URL)" "$(TARGET_URL)"
