#!/usr/bin/env python3
"""
Script to generate mock files from curl commands for the FastAPI mock server.
Usage: python generate_mock.py "curl_command_here"
"""

import re
import json
import os
from pathlib import Path
from urllib.parse import urlparse
import argparse

def parse_curl_command(curl_cmd):
    """Parse a curl command and extract method, URL, headers, and data."""
    
    # Remove 'curl' from the beginning
    curl_cmd = curl_cmd.strip()
    if curl_cmd.startswith('curl'):
        curl_cmd = curl_cmd[4:].strip()
    
    method = 'GET'  # default
    url = None
    headers = {}
    data = None
    form_data = {}
    
    # Parse method
    method_match = re.search(r'-X\s+(\w+)', curl_cmd)
    if method_match:
        method = method_match.group(1).upper()
        curl_cmd = curl_cmd.replace(method_match.group(0), '').strip()
    
    # Parse URL (usually the last argument or after -H headers)
    url_match = re.search(r'https?://[^\s]+', curl_cmd)
    if url_match:
        url = url_match.group(0)
    
    # Parse headers
    header_matches = re.findall(r'-H\s+["\']([^"\']+)["\']', curl_cmd)
    for header in header_matches:
        if ':' in header:
            key, value = header.split(':', 1)
            headers[key.strip()] = value.strip()
    
    # Parse JSON data (-d with JSON)
    # Find the position of -d and extract everything between quotes
    d_pos = curl_cmd.find('-d')
    if d_pos != -1:
        # Find the opening quote after -d
        quote_start = curl_cmd.find("'", d_pos)
        if quote_start == -1:
            quote_start = curl_cmd.find('"', d_pos)
        
        if quote_start != -1:
            # Find the closing quote
            quote_char = curl_cmd[quote_start]
            quote_end = curl_cmd.find(quote_char, quote_start + 1)
            
            if quote_end != -1:
                data_str = curl_cmd[quote_start + 1:quote_end]
                data_str = data_str.replace('\\"', '"')
                data_str = data_str.strip()
                
                try:
                    data = json.loads(data_str)
                except json.JSONDecodeError:
                    # Try to parse as form data
                    if '=' in data_str:
                        form_data = parse_form_data(data_str)
                    else:
                        data = data_str
    
    # Parse form data (-F)
    form_matches = re.findall(r'-F\s+["\']([^"\']+)["\']', curl_cmd)
    for form_match in form_matches:
        if '=' in form_match:
            key, value = form_match.split('=', 1)
            form_data[key.strip()] = value.strip()
    
    # Parse --data-raw
    data_raw_match = re.search(r'--data-raw\s+["\'](.+?)["\']', curl_cmd)
    if data_raw_match:
        data_str = data_raw_match.group(1)
        try:
            data = json.loads(data_str)
        except json.JSONDecodeError:
            data = data_str
    
    return {
        'method': method,
        'url': url,
        'headers': headers,
        'data': data,
        'form_data': form_data
    }

def parse_form_data(data_str):
    """Parse form data string into dictionary."""
    form_data = {}
    pairs = data_str.split('&')
    for pair in pairs:
        if '=' in pair:
            key, value = pair.split('=', 1)
            form_data[key.strip()] = value.strip()
    return form_data

def generate_mock_files(parsed_curl, output_dir='mocks'):
    """Generate mock files based on parsed curl command."""
    
    if not parsed_curl['url']:
        print("Error: No URL found in curl command")
        return False
    
    # Parse URL to get path
    parsed_url = urlparse(parsed_curl['url'])
    path = parsed_url.path.strip('/')
    
    # Create directory structure
    method = parsed_curl['method'].lower()
    endpoint_dir = Path(output_dir) / method / path.replace('/', '_')
    endpoint_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate request.json with method, endpoint, headers, and body data
    request_path = endpoint_dir / 'request.json'
    
    # Build request structure similar to existing pattern
    request_structure = {
        "method": parsed_curl['method'],
        "endpoint": f"/{path}",
        "headers": parsed_curl['headers']
    }
    
    # Add body data if available
    if parsed_curl['data']:
        request_structure["body"] = parsed_curl['data']
    elif parsed_curl['form_data']:
        request_structure["body"] = parsed_curl['form_data']
    
    with open(request_path, 'w') as f:
        json.dump(request_structure, f, indent=2)
    print(f"✓ Created {request_path}")
    
    # Generate response.json with sample data
    response_path = endpoint_dir / 'response.json'
    sample_response = generate_sample_response(parsed_curl['method'], path)
    
    with open(response_path, 'w') as f:
        json.dump(sample_response, f, indent=2)
    print(f"✓ Created {response_path}")
    
    return True

def generate_sample_response(method, path):
    """Generate a realistic sample response based on method and path."""
    
    # Common response patterns
    if method == 'GET':
        if 'user' in path.lower():
            return {
                "id": 1,
                "name": "John Doe",
                "email": "john@example.com",
                "created_at": "2024-01-01T00:00:00Z"
            }
        elif 'order' in path.lower():
            return {
                "order_id": "ORD-12345",
                "status": "pending",
                "total": 99.99,
                "items": [
                    {"id": 1, "name": "Product 1", "price": 49.99},
                    {"id": 2, "name": "Product 2", "price": 50.00}
                ]
            }
        else:
            return {
                "success": True,
                "data": "Sample response data",
                "timestamp": "2024-01-01T00:00:00Z"
            }
    
    elif method == 'POST':
        return {
            "success": True,
            "id": 12345,
            "message": "Resource created successfully",
            "created_at": "2024-01-01T00:00:00Z"
        }
    
    elif method == 'PUT':
        return {
            "success": True,
            "message": "Resource updated successfully",
            "updated_at": "2024-01-01T00:00:00Z"
        }
    
    elif method == 'DELETE':
        return {
            "success": True,
            "message": "Resource deleted successfully"
        }
    
    else:
        return {
            "success": True,
            "message": "Operation completed successfully"
        }

def main():
    parser = argparse.ArgumentParser(description='Generate mock files from curl commands')
    parser.add_argument('curl_command', help='The curl command to parse')
    parser.add_argument('--output-dir', default='mocks', help='Output directory for mock files')
    
    args = parser.parse_args()
    
    print("🔧 Parsing curl command...")
    parsed = parse_curl_command(args.curl_command)
    
    print(f"📋 Parsed details:")
    print(f"   Method: {parsed['method']}")
    print(f"   URL: {parsed['url']}")
    if parsed['headers']:
        print(f"   Headers: {parsed['headers']}")
    if parsed['data']:
        print(f"   JSON Data: {parsed['data']}")
    if parsed['form_data']:
        print(f"   Form Data: {parsed['form_data']}")
    
    print("\n📁 Generating mock files...")
    success = generate_mock_files(parsed, args.output_dir)
    
    if success:
        print("\n✅ Mock files generated successfully!")
        print(f"🌐 You can now test with: curl -X {parsed['method']} http://localhost:8000/{parsed['url'].split('/')[-1]}")
    else:
        print("\n❌ Failed to generate mock files")
        sys.exit(1)

if __name__ == '__main__':
    main() 