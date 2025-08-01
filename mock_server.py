from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import json
from pathlib import Path

app = FastAPI()

MOCKS_BASE_PATH = Path("./mocks")

def load_json(path: Path):
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def mock_handler(request: Request, full_path: str):
    method = request.method.lower()
    endpoint_dir = MOCKS_BASE_PATH / method / full_path.strip("/").replace("/", "_")

    # Load expected request and response
    expected_req_path = endpoint_dir / "request.json"
    response_path = endpoint_dir / "response.json"

    expected_request = load_json(expected_req_path)
    mock_response = load_json(response_path)

    if mock_response is None:
        return JSONResponse(
            status_code=404,
            content={"error": "Mock response not found", "path": str(response_path)},
        )

    # For methods with body, you can optionally validate input here
    if request.method in ["POST", "PUT", "PATCH"]:
        try:
            incoming_json = await request.json()
            # Optional: you can match expected_request with incoming_json if needed
        except Exception as e:
            return JSONResponse(
                status_code=400,
                content={"error": "Invalid incoming JSON", "details": str(e)},
            )

    return JSONResponse(content=mock_response)
