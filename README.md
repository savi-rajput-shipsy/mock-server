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

## Generate Mocks from Curl Commands

Use the included script to automatically generate mock files from curl commands:

```bash
# Generate mock for a GET request
python generate_mock.py "curl -X GET https://api.example.com/users/123"

# Generate mock for a POST request with JSON data
python generate_mock.py "curl -X POST https://api.example.com/users -H 'Content-Type: application/json' -d '{\"name\": \"John\", \"email\": \"john@example.com\"}'"

# Generate mock for a POST request with form data
python generate_mock.py "curl -X POST https://api.example.com/login -H 'Content-Type: application/x-www-form-urlencoded' -d 'username=john&password=secret123'"

# Generate mock for a PUT request
python generate_mock.py "curl -X PUT https://api.example.com/users/123 -H 'Content-Type: application/json' -d '{\"name\": \"Jane\"}'"

# Generate mock for a POST request with file upload
python generate_mock.py "curl -X POST https://api.example.com/upload -F 'file=@document.pdf' -F 'description=My document'"
```

The script will:
- Parse the curl command
- Create the appropriate directory structure
- Generate `request.json` (if request data exists)
- Generate `response.json` with realistic sample data

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
