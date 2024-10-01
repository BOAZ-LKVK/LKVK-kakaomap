import asyncio, re
from utils import *

async def parse(page, file, place):
    # 영업 시간 더 보기 버튼 클릭
    try:
        await page.click('//*[@class="gKP9i RMgN0"]')
    except:
        pass

    name         = await get_text_content(page,'//*[@class="GHAhO"]')
    category     = await get_text_content(page,'//*[@class="lnJFt"]')
    location     = await get_text_content(page,'//*[@class="LDgIH"]')
    contact      = await get_text_content(page,'//*[@class="xlx7Q"]')
    rank         = await get_text_content(page,'//*[@class="PXMot LXIwF"]')
    introduction = await get_text_content(page,'//*[@class="XtBbS"]')
    review_count = await get_text_content(page,'//*[@class="dAsGb"]')
    runtime      = await get_text_content(page,'//*[@class="gKP9i RMgN0"]')

    # rank 처리
    rank = re.search(r'별점([\d.]+)', rank).group(1) if rank else ""

    # review_count 처리
    review_count = re.search(r'방문자 리뷰 ([\d,]+)', review_count).group(1).replace(',','')

    # runtime 처리
    runtime = re.sub(r'(무|임|월|화|수|목|금|토)(?! )', r'\1 ', runtime)
    runtime = re.sub(r'(?<! )([월화수목금토])', r' \1', runtime)

    # langtitude, longitude
    locate_locator = page.get_by_role("button", name="길찾기")
    locate = await locate_locator.get_attribute('href', timeout=1000)

    latitude_match = re.search(r'latitude%5E([\d.]+)', locate)
    longitude_match = re.search(r'longitude%5E([\d.]+)', locate)

    latitude = latitude_match.group(1) if latitude_match else ""
    longitude = longitude_match.group(1) if longitude_match else ""

    name, category, location, contact, rank, introduction, review_count, runtime = replace_comma([name, category, location, contact, rank, introduction, review_count, runtime])
    file_write(file, [place, name, location, contact, rank, review_count, runtime, category, '', introduction, "네이버", latitude, longitude])


if __name__ == "__main__":
    item_list = extract_ids_from_txt('output.txt')
    filename = 'naver_place.csv'
    title = "가게 ID,가게 이름,가게 주소(위치),가게 연락처,가게 평점,리뷰 수,영업시간 정보,가게 카테고리(음식 종류),가격 정보,한 줄 소개,출처,latitude,longtitude\n"
    base_url = "/home"

    asyncio.run(do(item_list, filename, title, base_url, parse))