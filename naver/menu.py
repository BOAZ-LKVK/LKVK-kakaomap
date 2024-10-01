import asyncio, re
from playwright.async_api import async_playwright
from utils import *

async def parse(page, file, place):
    # 더보기 버튼(fvwqf) 누르기
    button_locator = page.locator('//*[@class="fvwqf"]')
    count = await button_locator.count()
    try :
        for i in range(count):
            button = button_locator.nth(i)
            await button.click()
    except :
        pass

    # 메뉴 가져오기
    menu_list = page.locator('.E2jtL')
    count = await menu_list.count()
    for i in range(count):
        menu = menu_list.nth(i)
        
        menu_name       = await get_text_content(menu, '.lPzHi')
        price           = await get_text_content(menu, '.GXS1X')
        description     = await get_text_content(menu,'.kPogF')
        try :
            image = await menu.get_by_alt_text(menu_name).get_attribute('src', timeout = 1000)
        except :
            image = ""

        price = price.replace(',','')
        menu_name, description, image = replace_comma([menu_name, description, image])
        file_write(file, [place, menu_name, price, description, image])
        
if __name__ == "__main__":

    item_list = extract_ids_from_txt('output.txt')
    filename = 'naver_menu.csv'
    title = "가게 ID,메뉴 이름,메뉴 가격,메뉴 사진 URL\n"
    url = "/menu/list"

    asyncio.run(do(item_list, filename, title, url, parse))
