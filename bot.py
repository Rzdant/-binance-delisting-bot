import os
import json
import urllib.request
import urllib.parse

def send_test_message():
    print("Executing bulletproof API transfer protocol...")
    
    # Secure token extraction
    token = os.environ.get("TELEGRAM_TOKEN")
    if not token:
        print("CRITICAL ERROR: TELEGRAM_TOKEN environment variable is missing on GitHub!")
        return
        
    # Clean any accidental spaces or hidden newline characters from the token string
    token = token.strip()
    
    # Destination parameters
    channel_id = "-1003704962476"
    text_content = "✅ **BULLETPROOF CONNECTION TEST SUCCESSFUL** ✅\n\nYour automated Python-to-Telegram data pipeline is working flawlessly."
    
    # Hardcoded, structurally validated API endpoint
    api_url = f"https://telegram.org{token}/sendMessage"
    
    # Build payload using strict data typing
    payload = {
        "chat_id": channel_id,
        "text": text_content,
        "parse_mode": "Markdown"
    }
    
    # Convert data dictionary to strict JSON format
    data_bytes = json.dumps(payload).encode('utf-8')
    
    # Construct headers to force server acceptance
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    try:
        # Open an independent web request pipeline
        req = urllib.request.Request(api_url, data=data_bytes, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=15) as response:
            response_code = response.getcode()
            response_body = response.read().decode('utf-8')
            print(f"Server Connection Established. Status Code: {response_code}")
            print(f"Response Metadata: {response_body}")
    except Exception as network_error:
        print(f"Network Pipeline Error: {network_error}")

if __name__ == "__main__":
    send_test_message()
