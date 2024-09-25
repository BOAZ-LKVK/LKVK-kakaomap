import os
import requests
import json
from bs4 import BeautifulSoup
from tqdm import tqdm

from utils.preprocess import get_data
from utils.constant import HEADERS, DATA

def get_rid_list(keyword_text):
    url = "https://im.diningcode.com/API/isearch/"
    DATA['query'] = keyword_text
    rid_list = []

    for idx in range(1, 6):
        DATA['page'] = idx  # 페이지 인덱스 설정
        response = requests.post(url, headers=HEADERS, data=DATA).json()
        items = response['result_data']['poi_section']['list']

        for item in items:
            v_rid = item['v_rid']
            rid_list.append(v_rid)

    return rid_list

def get_detail_data(rid_list):
    store_data_list = []
    menu_data_list = []
    review_data_list = []

    for v_rid in tqdm(rid_list):
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
        request_url = f"https://www.diningcode.com/profile.php?rid={v_rid}"
        response = requests.get(request_url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            store_info, menu_items, review_items = get_data(soup.body, v_rid)
            store_data_list.append(store_info)
            menu_data_list.extend(menu_items)
            review_data_list.extend(review_items)
        else:
            print(f"HTTP 요청 실패: 상태 코드 {response}")

    return store_data_list, menu_data_list, review_data_list