import os
import json
import urllib.request
import urllib.parse

def check_telegram_feed():
    print("🚀 Connecting to official Binance Telegram Announcement stream...")
    
    # Your verified bot credentials
    TOKEN = "8969427446:AAFXHvaggfzAJzV2B1pTKc-vWH7u-w5HaXM"
    channel_id = "-1003704962476"
    
    # We scrape the official Telegram web preview for Binance's broadcast channel
    target_url = "https://t.me"
    tg_api_url = f"https://telegram.org{TOKEN}/sendMessage"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        # Fetch the live stream text layout
        req = urllib.request.Request(target_url, headers=headers, method="GET")
        with urllib.request.urlopen(req, timeout=15) as response:
            html_content = response.read().decode('utf-8')
            
        print(f"Data stream pulled successfully. Character count: {len(html_content)}")
        
        # Split the text by message blocks to isolate individual posts
        message_blocks = html_content.split('class="tgme_widget_message_text')
        print(f"Analyzing the latest {len(message_blocks) - 1} announcements...")
        
        # Scan the most recent posts (skip the first split item as it's the header)
        for block in message_blocks[1:5]:
            # Extract just the readable text segment from the block
            clean_text = block.split('</div>')[0]
            clean_text = clean_text.replace('<br/>', '\n').strip()
            
            # STIRCT FILTER: Check for your delisting target words
            if "delist" in clean_text.lower() or "removal" in clean_text.lower():
                print("💥 MATCH FOUND: Processing alert transmission...")
                
                alert_msg = f"🚨 **NEW BINANCE DELISTING DETECTED** 🚨\n\n{clean_text}"
                
                # Secure parameter string assembly to prevent payload crashes
                query_data = urllib.parse.urlencode({
                    "chat_id": channel_id,
                    "text": alert_msg,
                    "parse_mode": "HTML"
                })
                
                final_dispatch_url = f"{tg_api_url}?{query_data}"
                tg_req = urllib.request.Request(final_dispatch_url, method="POST")
                with urllib.request.urlopen(tg_req, timeout=15) as resp:
                    print(f"Forward completed. Telegram Server Code: {resp.getcode()}")
                return # Exit after finding a match to prevent duplicates
                
        print("Scan finished. No active delisting pairs found in the latest message blocks.")
        
    except Exception as e:
        print(f"System Pipeline Error: {e}")

if __name__ == "__main__":
    check_telegram_feed()
