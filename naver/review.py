import asyncio, re
from playwright.async_api import async_playwright
from utils import *

async def parse(page, file, place):
    review_list = page.locator('.pui__X35jYm.EjjAW')
    count = await review_list.count()
    
    for i in range(count):
        review = review_list.nth(i)
        
        nickname    = await get_text_content(review,'//*[@class="pui__NMi-Dp"]')
        date        = await get_text_content(review,'//*[@class="pui__QKE5Pr"]')
        review_text = await get_text_content(review,'//*[@class="pui__vn15t2"]')

        date = re.search(r'\d{1,2}\.\d{1,2}\.[가-힣]', date).group()
        nickname, review_text = replace_comma([nickname, review_text])
        
        file_write(file, [place, nickname, date, review_text])


if __name__ == "__main__":

    item_list = extract_ids_from_txt('output.txt')
    filename = 'naver_review.csv'
    title = "가게 ID,닉네임,평점 정보,작성 날짜,리뷰 내용,추천 내용\n"
    base_url = "/review/visitor"

    asyncio.run(do(item_list, filename, title, base_url, parse))
