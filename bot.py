import os
import json
import urllib.request
import xml.etree.ElementTree as ET

def check_binance_delistings():
    print("🚀 Initializing Binance Delisting Monitor...")
    
    # Secure token extraction
    token = os.environ.get("TELEGRAM_TOKEN")
    if not token:
        print("CRITICAL ERROR: TELEGRAM_TOKEN environment variable is missing on GitHub!")
        return
    token = token.strip()
    
    # Configuration parameters
    channel_id = "-1003704962476"
    rss_url = "https://binance.com"
    
    # HARDCODED CORRECT API TARGET ENDPOINT (Bypasses parsing engine bugs)
    api_url = "https://telegram.org" + token + "/sendMessage"

    try:
        # Fetch data from Binance RSS Feed
        req_feed = urllib.request.Request(rss_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req_feed, timeout=15) as response:
            xml_data = response.read()
            
        root = ET.fromstring(xml_data)
        
        # Read the most recent 10 announcements
        for item in root.findall('.//item')[:10]:
            title = item.find('title').text
            link = item.find('link').text
            title_lower = title.lower()
            
            # VISUAL TEST FILTER: We look for 'delist', 'binance', or 'notice' 
            # so it triggers immediately for our test. 
            if "delist" in title_lower or "binance" in title_lower or "notice" in title_lower:
                message_text = f"🚨 **BINANCE ANNOUNCEMENT ALERT** 🚨\n\n{title}\n\n🔗 {link}"
                
                # Construct data packet
                payload = {
                    "chat_id": channel_id,
                    "text": message_text,
                    "parse_mode": "Markdown"
                }
                data_bytes = json.dumps(payload).encode('utf-8')
                headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
                
                # Fire request directly to Telegram API Server
                req_tg = urllib.request.Request(api_url, data=data_bytes, headers=headers, method="POST")
                with urllib.request.urlopen(req_tg, timeout=15) as tg_response:
                    print(f"Telegram Broadcast Successful! Status Code: {tg_response.getcode()}")

    except Exception as e:
        print(f"System execution error: {e}")

if __name__ == "__main__":
    check_binance_delistings()
