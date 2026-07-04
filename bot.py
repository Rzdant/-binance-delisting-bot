import os
import json
import urllib.request

def check_telegram_stream():
    print("🚀 Connecting to live Telegram Announcement server...")
    
    # Hardcoded with your verified bot parameters
    TOKEN = "8969427446:AAFXHvaggfzAJzV2B1pTKc-vWH7u-w5HaXM"
    channel_id = "-1003704962476"
    
    # Target URL and Telegram endpoint
    target_url = "https://t.me"
    tg_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    try:
        # Download the entire raw page text layout
        req = urllib.request.Request(target_url, headers=headers, method="GET")
        with urllib.request.urlopen(req, timeout=15) as response:
            raw_text = response.read().decode('utf-8').lower()
            
        print(f"Data stream scanned successfully. Size: {len(raw_text)} characters.")
        
        # TEST KEYWORD TRIGGER: Since "binance" is currently on the feed, this will force-match immediately.
        if "binance" in raw_text or "delist" in raw_text:
            print("💥 KEYWORD MATCHED! Dispatching alert payload...")
            
            alert_payload = {
                "chat_id": channel_id,
                "text": "🚨 **BINANCE SYSTEM ONLINE** 🚨\n\nYour automated data pipeline has successfully broken through. Telegram connection is verified!",
                "parse_mode": "Markdown"
            }
            
            data_bytes = json.dumps(alert_payload).encode('utf-8')
            tg_req = urllib.request.Request(tg_url, data=data_bytes, headers={"Content-Type": "application/json"}, method="POST")
            with urllib.request.urlopen(tg_req, timeout=15) as resp:
                print(f"Broadcast Complete! Server status code: {resp.getcode()}")
        else:
            print("No active matching keywords found in this stream block.")

    except Exception as error:
        print(f"Pipeline error log: {error}")

if __name__ == "__main__":
    check_telegram_stream()
