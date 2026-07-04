import os
import json
import urllib.request

def send_test_message():
    print("Initializing robust metadata injection protocol...")
    
    # Extract token cleanly
    token = os.environ.get("TELEGRAM_TOKEN")
    if not token:
        print("ERROR: TELEGRAM_TOKEN environment variable is missing!")
        return
    token = token.strip()
    
    # Destination params
    channel_id = "-1003704962476"
    text_content = "🚀 **CRITICAL PIPELINE UNLOCKED** 🚀\n\nYour GitHub cloud bot has successfully bypassed the network cache. Your data pipeline is now fully operational!"
    
    # EXTREME RESILIENCE: We split the URL to prevent the parsing engine from crashing on colons
    domain = "https://telegram.org"
    path = f"/bot{token}/sendMessage"
    full_target_url = domain + path
    
    payload = {
        "chat_id": channel_id,
        "text": text_content,
        "parse_mode": "Markdown"
    }
    
    data_bytes = json.dumps(payload).encode('utf-8')
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }
    
    try:
        req = urllib.request.Request(full_target_url, data=data_bytes, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=15) as response:
            print(f"Network Pipeline Secured. Server Status Code: {response.getcode()}")
            print(f"Server Payload: {response.read().decode('utf-8')}")
    except Exception as error_log:
        print(f"Execution Error: {error_log}")

if __name__ == "__main__":
    send_test_message()
