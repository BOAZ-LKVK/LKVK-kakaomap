HEADERS = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Content-Length": "169",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "im.diningcode.com",
        "Origin": "https://www.diningcode.com",
        "Referer": "https://www.diningcode.com/",
        "Sec-Ch-Ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
    }

DATA = {
    "query": "강남역",
    "addr": "",
    "keyword": "",
    "order": "r_score",
    "distance": "",
    "rn_search_flag": "on",
    "search_type": "poi_search",
    "lat": "",
    "lng": "",
    "rect": "",
    "s_type": "poi",
    "dc_flag": "1",
    "page": "1",
    "size": "20"
}

REVIEW_DATA = {
    'mode': 'LIST',
    'type': 'profile',
    'v_rid': '',
    'page': 2,
    'rows': 5,
    'start_id': 3
}

REVIEW_HEADERS = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Content-Length': '67',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'www.diningcode.com',
    'Origin': 'https://www.diningcode.com',
    'Referer': 'https://www.diningcode.com/profile.php?rid=',
    'Sec-Ch-Ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}
