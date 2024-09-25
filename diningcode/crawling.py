import pandas as pd 
from tqdm import tqdm
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE

from utils.utils import get_rid_list, get_detail_data


if __name__ == "__main__":
    area_list = ["선릉역", "선정릉역", "언주역", "강남역", "신논현역", "삼성역", "삼성중앙역", "양재역", "서초역", "교대역", "도곡역", "한티역" , "고속터미널역"]
    
    store_data = []
    menu_data = []
    review_data = []

    for area in tqdm(area_list):
        print(area, "크롤링 시작")
        # 음식점의 고유 번호인 rid를 가져옴.
        rid_list = get_rid_list(keyword_text = area)
        # rid번호를 이용해 음식점 상세 페이지로 이동해 크롤링 진행
        store_data_list, menu_data_list, review_data_list = get_detail_data(rid_list)
        # 데이터를 리스트에 저장
        store_data.extend(store_data_list)
        menu_data.extend(menu_data_list)
        review_data.extend(review_data_list)

    store_df = pd.DataFrame(store_data, columns=['가게ID','이름','주소','경도','위도','연락처','평점','리뷰수','영업시간','음식종류','태그', '특징'])
    menu_df = pd.DataFrame(menu_data, columns=['가게ID','메뉴이름', '가격', '사진_URL'])
    review_df = pd.DataFrame(review_data, columns=['가게ID','작성자', '평점', '작성일시', '리뷰내용'])

    # 전처리
    store_df[['영업시간', '음식종류', '태그', '특징']] = store_df[['영업시간', '음식종류', '태그', '특징']].astype(str)
    store_df = store_df.drop_duplicates()
    menu_df = menu_df.drop_duplicates()
    review_df = review_df.drop_duplicates()
    review_df['리뷰내용'] = review_df['리뷰내용'].apply(lambda x: ILLEGAL_CHARACTERS_RE.sub(r'', x))
    
    # 저장
    store_df.to_excel("./output_data/store.xlsx", index=False)
    menu_df.to_excel("./output_data/menu.xlsx", index=False)
    review_df.to_excel("./output_data/review.xlsx", index=False)