from datetime import datetime
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup

from utils.constant import REVIEW_DATA, REVIEW_HEADERS

# 함수 이름 뭐로 짓지...
def get_data(soup, v_rid):
    store_info = []
    menu_items = []
    review_items = []
    try:
        store_info = [v_rid]
        # =============================================================#
        # 음식점 이름
        title = soup.find('h1', class_='tit').get_text()
        store_info.append(title)
        # =============================================================#
        
        # =============================================================#
        # 주소 정보
        locat_li = soup.find('li', class_='locat')

        address_parts = [a.get_text(strip=True) for a in locat_li.find_all('a', recursive=False)]
        if not address_parts:
            address_parts = [a.get_text(strip=True) for a in locat_li.find_all('a')]

        address_detail_part = locat_li.find('span', recursive=False)
        if address_detail_part:
            address_parts.append(address_detail_part.get_text())     

        address = ' '.join(address_parts)
        store_info.append(address)
        # =============================================================#

        # =============================================================#
        # 음식점 위,경도
        latitude = 0
        longitude = 0  
        location_info = soup.find('div', class_='mini-map')
        if location_info:
            latitude = location_info.find('input', {'id': 'hdn_lat'})['value']
            longitude = location_info.find('input', {'id': 'hdn_lng'})['value']
        store_info.append(longitude)
        store_info.append(latitude)
        # =============================================================#

        # =============================================================#
        # 전화번호 추출
        tel_number = soup.find('li', class_='tel').get_text(strip=True)
        store_info.append(tel_number)
        # =============================================================#

        # =============================================================#
        # 리뷰 정보
        review_score = 0
        review_cnt = 0
        review_score_text = soup.find('strong', id='lbl_review_point')
        if review_score_text:
            review_score = review_score_text.get_text()
            review_cnt_text = soup.find('span', class_='review_count').get_text()
            pattern = r'\d+'
            review_cnt = re.search(pattern, review_cnt_text).group()
            
        store_info.append(review_score)
        store_info.append(review_cnt)
        # =============================================================#

        # =============================================================#
        # 영업 정보 추출
        # 오늘 영업 정보 
        opening_hours = {}
        weekday = datetime.today().weekday()
        today_hours_div = soup.find('div', class_='busi-hours-today')
        if today_hours_div:
            today_hours_ul = today_hours_div.find('ul', class_='list')
            today_hours_p = today_hours_ul.find_all('p', class_="r-txt")
            today_hours = [info.get_text(strip=True) for info in today_hours_p]
            opening_hours[weekday] = today_hours

            # 나머지 영업 정보 가져오기
            busi_hours_div = soup.find('div', class_='busi-hours')
            ul_list = busi_hours_div.find('ul', class_='list') if busi_hours_div else None
            all_elements = ul_list.find_all(recursive=False) if ul_list else []
            current_group = []
            for element in all_elements:
                if element.name == 'hr':
                    if current_group:
                        weekday = (weekday + 1) % 7
                        opening_hours[weekday] = current_group
                        current_group = []
                else:
                    time_info = element.find('p', class_="r-txt").get_text(strip=True)
                    current_group.append(time_info)

            # 마지막 요일 추가
            weekday = (weekday + 1) % 7
            opening_hours[weekday] = current_group
            store_info.append(opening_hours)
        else:
            store_info.append("시간정보가 없습니다.")
        # =============================================================#

        # =============================================================#
        # 대표 메뉴들
        btxt_links = soup.find_all('a', class_='btxt')
        categories = [a.get_text(strip=True) for a in btxt_links]
        store_info.append(categories)
        # =============================================================#

        # =============================================================#
        # 해시태그 추출
        tags_li = soup.find('li', class_='tag')
        char_li = soup.find('li', class_='char')
        hashtags = [a.get_text(strip=True) for a in tags_li.find_all('a')]
        characteristics = [a.get_text(strip=True) for a in char_li.find_all('a')]
        store_info.append(hashtags)
        store_info.append(characteristics)
        # =============================================================#

        # =============================================================#    
        # '메뉴 추출
        menu_list = soup.find('ul', class_='list Restaurant_MenuList')

        if menu_list:
            menu_elements = menu_list.find_all('li')

            for element in menu_elements:
                menu_name = element.find('p', class_='l-txt Restaurant_MenuItem').get_text(strip=True)
                menu_price = element.find('p', class_='r-txt Restaurant_MenuPrice').get_text(strip=True)
                menu = [v_rid, menu_name, menu_price, "None"]
                menu_items.append(menu)
        # =============================================================#    

        # =============================================================#    
        # 리뷰 추출
        if review_cnt != 0:
            review_list = soup.find('div', id='div_review')
            if review_list:
                review_items.extend(preprocess_review(review_list, v_rid))
            # UI에 나오는 review 말고 Query를 날려서 Review 데이터 크롤링.
            review_items.extend(request_review_data(v_rid, review_cnt))
        # =============================================================#    
    except Exception as e:
        print(v_rid,"에서 문제가 발생")
        print(e)

    return store_info, menu_items, review_items


def request_review_data(v_rid, total_review_cnt):
    request_url = "https://www.diningcode.com/2018/ajax/review.php"
    
    REVIEW_DATA['v_rid'] = v_rid
    REVIEW_DATA['rows'] = {int(total_review_cnt) - 3}
    REVIEW_HEADERS['Referer'] =  f'https://www.diningcode.com/profile.php?rid={v_rid}'
    
    response = requests.post(request_url, headers=REVIEW_HEADERS, data=REVIEW_DATA)
    review_soup = BeautifulSoup(response.text, 'html.parser')
    review_lists = preprocess_review(review_soup, v_rid)

    return review_lists

def preprocess_review(review_html, v_rid):
    review_elements = review_html.find_all('div', class_="latter-graph")

    review_lists = []

    for review_element in review_elements:
        nickname = review_element.find('p', class_='person-grade').find('strong').text
        point_detail = review_element.find('span', class_='total_score')
        if point_detail:
            review_score = review_element.find('span', class_='total_score').get_text()
            date = review_element.find('div', class_='date').text.strip()
            review_content = review_element.find('p', class_='review_contents btxt').text.strip()
            # review_item
            review_item = [v_rid, nickname, review_score, date, review_content]
            review_lists.append(review_item)
        else:
            print("review가 숨김처리 되어있습니다.")    
    return review_lists