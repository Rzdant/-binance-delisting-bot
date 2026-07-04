import os
import json
import urllib.request

def check_binance_delistings():
    print("🚀 Initializing Firewall-Proof Query Engine...")
    
    # Secure token extraction
    token = os.environ.get("TELEGRAM_TOKEN")
    if not token:
        print("CRITICAL ERROR: TELEGRAM_TOKEN environment variable is missing on GitHub!")
        return
    token = token.strip()
    
    channel_id = "-1003704962476"
    
    # BULLETPROOF GET ENDPOINT: Avoids POST payload filters entirely
    catalog_url = "https://binance.com"
    tg_url = f"https://telegram.org{token}/sendMessage"
    
    # Real-world browser signatures prevent cloud filtering
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Lang": "en"
    }

    try:
        # Request data stream using standard GET protocol
        req = urllib.request.Request(catalog_url, headers=headers, method="GET")
        with urllib.request.urlopen(req, timeout=15) as response:
            raw_data = response.read().decode('utf-8')
            
        # Parse standard JSON data block
        raw_json = json.loads(raw_data)
        articles = raw_json.get("data", {}).get("articles", [])
        
        print(f"Successfully connected to backend. Retrieved {len(articles)} active announcements.")
        
        for article in articles:
            title = article.get("title", "")
            code = article.get("code", "")
            
            # Reconstruct the direct hyperlink using Binance CMS parameters
            link = f"https://www.binance.com/en/support/announcement/{code}"
            title_lower = title.lower()
            
            # STABLE PRODUCTION FILTER: Checks for delistings exclusively
            # Triggers on words like "delist", "removal of trading pairs", etc.
            if "delist" in title_lower or "removal" in title_lower:
                message_text = f"🚨 **BINANCE DELISTING ALERT** 🚨\n\n{title}\n\n🔗 {link}"
                
                tg_payload = {
                    "chat_id": channel_id,
                    "text": message_text,
                    "parse_mode": "Markdown"
                }
                
                tg_bytes = json.dumps(tg_payload).encode('utf-8')
                tg_req = urllib.request.Request(tg_url, data=tg_bytes, headers={"Content-Type": "application/json"}, method="POST")
                
                with urllib.request.urlopen(tg_req, timeout=15) as tg_resp:
                    print(f"Telegram Broadcast Successful! Status Code: {tg_resp.getcode()}")

    except Exception as e:
        print(f"System execution error: {e}")

if __name__ == "__main__":
    check_binance_delistings()
