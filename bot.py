import os
import json
import urllib.request
import re

def check_direct_binance_stream():
    print("🚀 Connecting natively to Binance Telegram Web Preview...")
    
    TOKEN = "8969427446:AAFXHvaggfzAJzV2B1pTKc-vWH7u-w5HaXM"
    channel_id = "@del_bin_phy"
    
    # Target the clean public web-history preview
    binance_channel_handle = "binance_announcements" 
    target_url = f"https://t.me{binance_channel_handle}"
    
    # FIXED: Added the required 'api.' subdomain
    final_tg_url = f"https://telegram.org{TOKEN}/sendMessage"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        req = urllib.request.Request(target_url, headers=headers, method="GET")
        with urllib.request.urlopen(req, timeout=15) as response:
            raw_html = response.read().decode('utf-8')
            
        print(f"Data stream acquired successfully. Character total: {len(raw_html)}")
        
        # Scrapes the individual message items out of the HTML timeline
        messages = re.findall(r'data-post="[^"]+/(\d+)".*?<div class="tgme_widget_message_text[^"]*"[^>]*>(.*?)</div>', raw_html, re.DOTALL)
        
        if not messages:
            print("Could not parse message streams from layout. Trying global fallback scan...")
            raw_text = raw_html.lower()
            if "delist" in raw_text or "remove" in raw_text:
                trigger_alert(final_tg_url, channel_id)
            return

        # Scan the absolute latest message to prevent constant looping spam
        latest_msg_id, latest_msg_text = messages[-1]
        latest_msg_text_lower = latest_msg_text.lower()
        
        state_file = "last_id.txt"
        last_seen_id = ""
        if os.path.exists(state_file):
            with open(state_file, "r") as f:
                last_seen_id = f.read().strip()
                
        if latest_msg_id == last_seen_id:
            print(f"Scan complete. No new messages since ID {latest_msg_id}.")
            return

        with open(state_file, "w") as f:
            f.write(latest_msg_id)

        if "delist" in latest_msg_text_lower or "remove" in latest_msg_text_lower:
            trigger_alert(final_tg_url, channel_id)
        else:
            print(f"New post found (ID {latest_msg_id}), but no keywords matched. Skipping alert.")

    except Exception as e:
        print(f"Pipeline Execution Error: {e}")

def trigger_alert(url, chat_id):
    print("💥 ALARM TRIGGERED: Keywords matched!")
    payload = {
        "chat_id": chat_id,
        "text": "🚨 **NEW OFFICIAL BINANCE REMOVAL NOTICE** 🚨\n\nA new asset delisting or trading pair removal announcement has been issued. Check the channel layout immediately."
    }
    data_bytes = json.dumps(payload).encode('utf-8')
    tg_req = urllib.request.Request(url, data=data_bytes, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(tg_req, timeout=15) as resp:
        print(f"Alert successfully broadcasted! Server Code: {resp.getcode()}")

if __name__ == "__main__":
    check_direct_binance_stream()
