from playwright.async_api import async_playwright

def extract_ids_from_txt(filename):
    ids = []
    
    # 텍스트 파일 읽기
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        
        # 각 줄에서 숫자 ID 추출
        for line in lines:
            # '/restaurant/' 이후 '?' 이전의 숫자만 추출
            start_idx = line.find('/restaurant/') + len('/restaurant/')
            end_idx = line.find('?')
            if start_idx != -1 and end_idx != -1:
                restaurant_id = line[start_idx:end_idx]
                ids.append(restaurant_id)
    
    return ids

async def get_text_content(page, locator_selector):
    try:
        locator = page.locator(locator_selector)
        # 요소가 존재하는지 확인
        if await locator.count() > 0:
            # 텍스트 내용을 가져오고 빈 문자열이 아닌 경우 반환
            text = await locator.text_content()
            return text.strip() if text else ""
        return ""
    except :
        return ""
    
async def get_all_text_contents(page, locator_selector):
    try:
        locator = page.locator(locator_selector)
        # 요소가 존재하는지 확인
        if await locator.count() > 0:
            # 텍스트 내용을 가져오고 빈 문자열이 아닌 경우 반환
            text_list = await locator.all_text_contents()
            text = ' '.join([r.text.replace("\n", " ") for r in text_list])
            return text.strip() if text else ""
        return ""
    except :
        return ""
    
def replace_comma(text_list) :
    result = []
    for text in text_list :
        result.append(text.replace(',',' ').replace('\n',' '))
    return result

def file_write(file, item_list) :
    for item in item_list :
        file.write(item+',')
    file.write("\n")

async def do(item_list, filename, title, url, parse):
    # 파일 열기
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(title)
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()

            for item in item_list:
                base_url = f"https://m.place.naver.com/restaurant/{item}{url}"
                await page.goto(base_url)
                await page.wait_for_timeout(3000)  # 1초 대기

                # parse 함수 호출
                await parse(page, file, item)
            await browser.close()

def remove_duplicates_from_txt(input_filename, output_filename):
    unique_lines = set()

    with open(input_filename, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

        for line in lines:
            clean_line = line.strip() 
            if clean_line: 
                unique_lines.add(clean_line)

    with open(output_filename, 'w', encoding='utf-8') as outfile:
        for line in sorted(unique_lines): 
            outfile.write(line + '\n')
