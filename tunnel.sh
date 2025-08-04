#!/bin/bash

echo "Starting Cloudflare tunnel for mock server..."
echo "This will create an HTTPS URL for your local server on port 8000"
echo ""

# Start the tunnel
cloudflared tunnel --url http://localhost:8000 