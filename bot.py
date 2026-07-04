import sys
import os
import json
import urllib.request

def process_and_send():
    token = os.environ.get("TELEGRAM_TOKEN")
    if not token:
        print("Missing token.")
        return
    token = token.strip()
    
    raw_html = sys.stdin.read()
    channel_id = "-1003704962476"
    tg_url = f"https://telegram.org{token}/sendMessage"

    # Print a tiny chunk to the log so we can see the data layout
    print(f"Scraper Data Stream Check (First 150 chars): {raw_html[:150]}")

    # BROAD VERIFICATION FILTER: Check for normal keywords
    if "delist" in raw_html.lower() or "binance" in raw_html.lower() or "announcement" in raw_html.lower():
        alert_text = "🚨 **BINANCE SYSTEM ONLINE** 🚨\n\nYour keyword filter successfully matched text in the live database! The connection is 100% established."
        
        payload = {"chat_id": channel_id, "text": alert_text, "parse_mode": "Markdown"}
        data_bytes = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(tg_url, data=data_bytes, headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=15) as resp:
            print(f"Alert transmitted to Telegram! Server code: {resp.getcode()}")
    else:
        # FORCED FALLBACK: If keywords are hidden, force send a confirmation message anyway
        print("Keywords not found in raw block, executing emergency notification override...")
        fallback_text = "⚠️ **BOT TESTING PIPELINE OVERRIDE** ⚠️\n\nThe script ran successfully without errors, but the website text is hidden behind Javascript. Telegram connection is verified."
        
        payload = {"chat_id": channel_id, "text": fallback_text, "parse_mode": "Markdown"}
        data_bytes = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(tg_url, data=data_bytes, headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=15) as resp:
            print(f"Emergency text transmitted! Server code: {resp.getcode()}")

if __name__ == "__main__":
    process_and_send()
