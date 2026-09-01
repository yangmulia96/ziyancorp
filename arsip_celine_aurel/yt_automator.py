import os
import sys
import time
import subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(r"C:\Users\arija\ziyancorp\arsip_celine_aurel")
USER_DATA_DIR = ROOT / "yt_user_data"

def upload_youtube_shorts_automator(video_path: str, title: str, description: str) -> dict:
    if not os.path.exists(video_path):
        return {"status": "error", "reason": f"file_not_found: {video_path}"}
        
    with sync_playwright() as p:
        try:
            # Persistent context using saved user profile
            context = p.chromium.launch_persistent_context(
                user_data_dir=str(USER_DATA_DIR),
                headless=False,
                args=["--disable-blink-features=AutomationControlled"]
            )
            page = context.pages[0] if context.pages else context.new_page()
            
            target_url = "https://studio.youtube.com/channel/UC0h3xyafx6P6J_CjpzhpSeg"
            print("Navigating to Celine Aurel YouTube Studio:", target_url)
            page.goto(target_url, wait_until="domcontentloaded")
            page.wait_for_timeout(3000)
            
            print("Opening upload dialog...")
            try:
                page.click("#create-icon", timeout=5000)
                page.click("#text-item-0", timeout=5000)
            except Exception:
                page.goto("https://studio.youtube.com/channel/UC0h3xyafx6P6J_CjpzhpSeg/videos/upload?d=ud")
                
            page.wait_for_timeout(2000)
            
            print("Uploading file:", video_path)
            file_input = page.locator('input[type="file"]')
            file_input.set_input_files(video_path)
            page.wait_for_timeout(5000)
            
            print("Filling metadata...")
            try:
                title_box = page.locator("#title-textarea #textbox")
                title_box.fill(title[:100])
            except Exception as e:
                print("Title note:", e)
                
            try:
                desc_box = page.locator("#description-textarea #textbox")
                desc_box.fill(description[:4000])
            except Exception as e:
                print("Desc note:", e)
                
            try:
                page.click('tp-yt-paper-radio-button[name="VIDEO_MADE_FOR_KIDS_NOT_MFK"]', timeout=5000)
            except Exception as e:
                print("Kids note:", e)
                
            page.wait_for_timeout(2000)
            
            for _ in range(3):
                try:
                    page.click("#next-button", timeout=5000)
                    page.wait_for_timeout(2000)
                except Exception:
                    pass
                    
            try:
                page.click('tp-yt-paper-radio-button[name="PUBLIC"]', timeout=5000)
            except Exception:
                pass
                
            page.wait_for_timeout(1000)
            
            try:
                page.click("#done-button", timeout=5000)
                print("Clicked Publish button!")
            except Exception as e:
                print("Done note:", e)
                
            page.wait_for_timeout(5000)
            context.close()
            return {"status": "success", "note": "Uploaded live to Celine Aurel YouTube Studio!"}
        except Exception as e:
            return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    vid = r"C:\Users\arija\Downloads\fashion_assets\Woman_walking_in_jeans_202608071926.mp4"
    res = upload_youtube_shorts_automator(
        vid,
        "Celine Aurel Official Shorts #Shorts",
        "Koleksi fashion Celine Aurel resmi.\n\n#Shorts #CelineAurel"
    )
    print("RESULT:", res)
