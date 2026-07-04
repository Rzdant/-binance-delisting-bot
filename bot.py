import os
import json
import urllib.request

def check_direct_binance_stream():
    print("🚀 Connecting natively to official Binance Announcement feed...")
    
    # Fully audited credentials
    TOKEN = "8969427446:AAFXHvaggfzAJzV2B1pTKc-vWH7u-w5HaXM"
    channel_id = "@del_bin_phy"
    
    target_url = "https://t.me"
    
    # End-to-end clean string endpoint layout
    api_domain = "https://telegram.org"
    api_path = "/bot" + TOKEN + "/sendMessage"
    final_tg_url = api_domain + api_path
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        # Secure data stream straight from the native source
        req = urllib.request.Request(target_url, headers=headers, method="GET")
        with urllib.request.urlopen(req, timeout=15) as response:
            # Converts the entire document layout into completely lowercase letters
            raw_text = response.read().decode('utf-8').lower()
            
        print(f"Data stream acquired successfully. Character total: {len(raw_text)}")
        
        # -------------------------------------------------------------------------
        # FINAL PRODUCTION FILTER: Monitors strictly for 'delist' and 'remove'
        # -------------------------------------------------------------------------
        if "delist" in raw_text or "remove" in raw_text:
            print("💥 ALARM TRIGGERED: Official Binance target vocabulary matched!")
            
            payload = {
                "chat_id": channel_id,
                "text": "🚨 **OFFICIAL BINANCE REMOVAL NOTICE** 🚨\n\nA new asset delisting or trading pair removal announcement has been issued directly on the official wire. Please review the announcement channel immediately."
            }
            
            data_bytes = json.dumps(payload).encode('utf-8')
            tg_req = urllib.request.Request(
                final_tg_url, 
                data=data_bytes, 
                headers={"Content-Type": "application/json"}, 
                method="POST"
            )
            
            with urllib.request.urlopen(tg_req, timeout=15) as resp:
                print(f"Alert successfully broadcasted! Server Code: {resp.getcode()}")
        else:
            print("Scan complete. Zero active delisting or removal notices found in this block.")

    except Exception as e:
        print(f"Pipeline Execution Error: {e}")

if __name__ == "__main__":
    check_direct_binance_stream()
