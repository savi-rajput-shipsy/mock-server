# FastAPI Mock Server

A simple file-based mock server using FastAPI. Serve mock API responses for development and testing.

## Quick Start

1. **Install dependencies:**
   ```sh
   pip install fastapi uvicorn
   ```

2. **Run the server:**
   ```sh
   python3 -m uvicorn mock_server:app --reload --port 8000
   ```

3. **Expose locally with ngrok:**
   - [Download ngrok](https://ngrok.com/download)
   - Add your authtoken:
     ```sh
     ngrok config add-authtoken <token>
     ```
   - Start ngrok tunnel:
     ```sh
     ngrok http 8000
     ```

## Directory Structure


```
mocks/
  get/
    api_RiderApp_riderState/
      request.json      # (optional) expected request structure
      response.json     # mock response for GET /api/RiderApp/riderState
  post/
    another_endpoint/
      request.json
      response.json
```

Example for GET /api/RiderApp/riderState:

```
mocks/get/api_RiderApp_riderState/response.json
```

Contents of `response.json` (example):

```json
{
  "status": "active",
  "location": "downtown"
}
```

- Organize mocks by HTTP method and endpoint.
- Edit `request.json` and `response.json` as needed for your API mocks.

---
