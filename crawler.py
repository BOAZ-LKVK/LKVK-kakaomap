from playwright.sync_api import sync_playwright
import json
import re
import csv
from items.Menu import Menu
from items.Review import Review
from items.Shop import Shop

def get_review(_id_str, _page, _shop_name, _review_cnt):
    if _review_cnt > 3:
        while _page.locator("div.evaluation_review a.link_more.link_unfold").count() == 0:
            _page.click("div.evaluation_review a.link_more")
            _page.wait_for_timeout(300)

    evaluation_items = _page.locator('div.evaluation_review ul.list_evaluation li')
    review_list = []
    for evaluation in evaluation_items.element_handles():
        if evaluation.query_selector("div.unit_info div.inner_user span.txt_username") is None:
            continue

        _username = evaluation.query_selector("div.unit_info div.inner_user span.txt_username").inner_text()
        _star_css_str = evaluation.query_selector("div.star_info span.ico_star.inner_star").get_attribute("style")
        _star = int(_star_css_str.replace('width:', '').replace('%;', '').strip()) / 20
        _comment = evaluation.query_selector("div.comment_info p.txt_comment span").inner_text()
        _time_write = evaluation.query_selector("div.unit_info span.time_write").inner_text()

        review = Review(
            id_str=_id_str,
            shop_name=_shop_name,
            username=_username,
            star=_star,
            time=_time_write,
            comment=_comment
        )
        with open('./output_data/review.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                review.id_str,
                review.shop_name,
                review.username,
                review.star,
                review.time,
                review.comment
            ])
    return review_list


def get_menu(_id_str, _page, _shop_name):
    menu_elements = _page.locator('div#mArticle div.cont_menu ul.list_menu li')
    menu_list = []
    menu_name_list = []
    for menu_element in menu_elements.element_handles():
        info_menu = menu_element.query_selector("div.info_menu")
        _name = info_menu.query_selector("span.loss_word").inner_text()
        _price_element = info_menu.query_selector("em.price_menu")
        _price = "" if _price_element is None else _price_element.inner_text()[4:]
        link_photo = menu_element.query_selector("a.link_photo")
        _url = "" if link_photo is None else "https:" + link_photo.query_selector("span.inner_photo img.img_thumb").get_attribute("src")

        menu = Menu(
            id_str=_id_str,
            shop_name=_shop_name,
            name=_name,
            price=_price,
            url=_url
        )

        menu_list.append(menu)
        menu_name_list.append(_name)
        with open('./output_data/menu.csv', 'a', newline='',encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([menu.id_str,
                menu.shop_name,
                menu.name,
                menu.price,
                menu.url])
    return menu_list, menu_name_list
if __name__ == "__main__":
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        detail_item = {}
        with open('id_list.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                id_list = list(map(int, row))
        for id_str in id_list:
            detail_url = "https://place.map.kakao.com/" + str(id_str)
            detail_page = context.new_page()
            detail_page.goto(detail_url)
            detail_page.wait_for_load_state("networkidle")

            title_element = detail_page.query_selector("div#mArticle div.inner_place h2.tit_location")
            title = "" if  title_element is None else title_element.inner_text()

            address_element = detail_page.query_selector("div#mArticle div.details_placeinfo div.placeinfo_default div.location_detail span.txt_address")
            address = "" if address_element is None else address_element.inner_text()

            contact_element = detail_page.query_selector("div#mArticle div.details_placeinfo div.placeinfo_default.placeinfo_contact div.location_detail span.txt_contact")
            contact = "" if contact_element is None else contact_element.inner_text()

            star_element = detail_page.query_selector("div#mArticle div.place_details div.location_evaluation span.color_b")
            star = "" if star_element is None else star_element.inner_text()

            category_element = detail_page.query_selector("div#mArticle div.place_details div.location_evaluation span.txt_location")
            category = "" if category_element is None else category_element.inner_text()[4:]

            review_cnt_element = detail_page.query_selector("div#mArticle strong.total_evaluation span.color_b")
            open_time_list = detail_page.query_selector_all(
                "div#mArticle div.details_placeinfo div.placeinfo_default div.location_detail.openhour_wrap div.location_present span.txt_operation")
            open_time = ""
            for open_time_element in open_time_list:
                open_time += open_time_element.inner_text()

            review_cnt = 0
            review_list = []
            if review_cnt_element:
                review_cnt = int(review_cnt_element.inner_text())
                review_list = get_review(id_str, detail_page, title, review_cnt)

            menu_list = []
            menu_name_list = []
            menu_page = detail_page.query_selector("div#mArticle div.cont_menu")
            if menu_page:
                menu_list, menu_name_list = get_menu(id_str, detail_page, title)

            shop = Shop(
                id_str=id_str,
                name=title,
                address=address,
                contact=contact,
                star=star,
                review_cnt=review_cnt,
                time=open_time,
                category=category,
                menu_list=menu_name_list,
                source="kakao map",
            )
            with open('./output_data/shop.csv', 'a', newline='',encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([
                        shop.id_str,
                        shop.name,
                        shop.address,
                        shop.contact,
                        shop.star,
                        shop.review_cnt,
                        shop.time,
                        shop.category,
                        json.dumps(shop.menu_list),  # 메뉴 리스트를 쉼표로 구분하여 하나의 문자열로 변환
                        shop.source
                    ])
            detail_page.close()