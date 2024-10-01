import asyncio
import time
from utils import *

def get_location(filename):
    base_url = "list?query=맛집"
    urls = []

    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            lat, lon = line.strip().split(',')[1:3]
            urls.append(f"{base_url}&x={lon}&y={lat}")

    return urls[1:]

async def parse(page, file,item) :
    await page.click('.AtjOO')

    for _ in range(10): 
        await page.mouse.wheel(0, 10000)
        await page.wait_for_timeout(1000) 

        hrefs = await page.locator('//*[@class="tzwk0"]').evaluate_all('elements => elements.map(e => e.getAttribute("href"))')
            
        for href in hrefs:
            file.write(href + '\n')

if __name__ == "__main__":
    item_list = get_location('location.csv')
    filename = 'output.txt'
    title = ""
    url = ""

    asyncio.run(do(item_list, filename, title, url, parse))
