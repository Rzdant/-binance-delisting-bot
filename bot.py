import os
import json
import urllib.request

def process_and_send():
    # Hardcoded with your verified token string
    TOKEN = "8969427446:AAFXHvaggfzAJzV2B1pTKc-vWH7u-w5HaXM"
    channel_id = "-1003704962476"
    tg_url = f"https://telegram.org{TOKEN}/sendMessage"
    
    # DIRECT LIVE BACKEND API STREAM (Completely bypasses HTML and scraping caches)
    catalog_url = "https://binance.com"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Lang": "en"
    }

    try:
        # Establish raw GET request pipeline directly to the database endpoint
        req = urllib.request.Request(catalog_url, headers=headers, method="GET")
        with urllib.request.urlopen(req, timeout=15) as response:
            raw_data = response.read().decode('utf-8')
            
        raw_json = json.loads(raw_data)
        articles = raw_json.get("data", {}).get("articles", [])
        
        print(f"Network Pipeline Active. Successfully scanned {len(articles)} live announcements.")
        
        for article in articles:
            title = article.get("title", "")
            code = article.get("code", "")
            link = f"https://binance.com{code}"
            title_lower = title.lower()
            
            # BROAD TEMPORARY VERIFICATION FILTER: Check for "vip", "airdrop", or "delist"
            # This ensures we get matches from the live database right now to test the delivery path.
            if any(keyword in title_lower for keyword in ["delist", "removal", "vip", "airdrop"]):
                print(f"Match found: {title}")
                alert_text = f"🚨 **BINANCE LIVE EVENT DETECTED** 🚨\n\n{title}\n\n🔗 {link}"
                
                payload = {
                    "chat_id": channel_id,
                    "text": alert_text,
                    "parse_mode": "Markdown"
                }
                
                data_bytes = json.dumps(payload).encode('utf-8')
                tg_req = urllib.request.Request(tg_url, data=data_bytes, headers={"Content-Type": "application/json"}, method="POST")
                with urllib.request.urlopen(tg_req, timeout=15) as resp:
                    print(f"Alert successfully broadcasted! Server code: {resp.getcode()}")
                    
    except Exception as e:
        print(f"Pipeline execution crash: {e}")

if __name__ == "__main__":
    process_and_send()
