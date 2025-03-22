import asyncio
import pandas as pd
import os
from datetime import datetime
import time
from playwright.async_api import async_playwright

CSV_FILE = "./data/xp_points_final.csv"

async def scrape_duolingo_continuous():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True) 
        page = await browser.new_page()
        await page.goto("https://bringback.duolingo.com/", timeout=60000)

        print("Page loaded. Starting to fetch XP every minute...")
        time.sleep(10)
        while True:
            try:
                xp_text = await page.text_content(".Profile_xp-text-dead-duo__87OV2")
            except:
                xp_text = "Class not found"

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  

            new_data = pd.DataFrame([[timestamp, xp_text]], columns=["Timestamp", "XP"])

            if not os.path.exists(CSV_FILE):
                new_data.to_csv(CSV_FILE, index=False)  
            else:
                new_data.to_csv(CSV_FILE, mode="a", header=False, index=False)  

            print(f"Saved XP: {xp_text} at {timestamp}")

            await asyncio.sleep(60) 

async def main():
    await scrape_duolingo_continuous()

    try:
        asyncio.get_running_loop()
        asyncio.create_task(main()) 
    except RuntimeError:
        asyncio.run(main()) 