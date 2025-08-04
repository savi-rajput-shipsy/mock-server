.PHONY: start dev

start:
	python3 -m uvicorn mock_server:app --reload --port 8000

dev: start 