import os
import json
import urllib.request

def check_binance_delistings():
    print("🚀 Initializing Cloudflare-Proof Binance Monitor...")
    
    # Secure token extraction
    token = os.environ.get("TELEGRAM_TOKEN")
    if not token:
        print("CRITICAL ERROR: TELEGRAM_TOKEN environment variable is missing on GitHub!")
        return
    token = token.strip()
    
    channel_id = "-1003704962476"
    
    # We target the official API catalog endpoint to completely bypass Cloudflare blocks
    api_list_url = "https://binance.com"
    tg_url = f"https://telegram.org{token}/sendMessage"
    
    # Strict API Payload Request Structure
    payload_data = {
        "catalogId": 49, # Catalog 49 explicitly targets the "Latest Binance News" database
        "pageNo": 1,
        "pageSize": 10
    }
    
    data_bytes = json.dumps(payload_data).encode('utf-8')
    
    # Authentic headers mimic a normal browser request
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Lang": "en"
    }

    try:
        # Request the database directly
        req = urllib.request.Request(api_list_url, data=data_bytes, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=15) as response:
            raw_json = json.loads(response.read().decode('utf-8'))
            
        articles = raw_json.get("data", {}).get("catalogs", [{}])[0].get("articles", [])
        print(f"Successfully processed {len(articles)} announcements from Binance backend.")
        
        for article in articles:
            title = article.get("title", "")
            code = article.get("code", "")
            # Reconstruct the direct link format using the distinct database article string code
            link = f"https://www.binance.com/en/support/announcement/{code}"
            title_lower = title.lower()
            
            # BROAD PRODUCTION FILTER: Tracks "delist", "removal", "notice", and "binance"
            # This ensures we get data right away to verify the connection works.
            if any(word in title_lower for word in ["delist", "removal", "notice", "binance"]):
                message_text = f"🚨 **BINANCE ANNOUNCEMENT ALERT** 🚨\n\n{title}\n\n🔗 {link}"
                
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
