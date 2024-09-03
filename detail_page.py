from playwright.sync_api import sync_playwright
import json
import re

# 리스트를 사용하여 모든 응답을 저장
responses = []
id_list = []

# Define a callback function to handle responses
def handle_response(response):
    if "clickpoi-map.kakao.com/click/v1/poi.json" in response.url:
        responses.append(response)

if __name__ == "__main__":
    with sync_playwright() as pw:
        # browser = pw.chromium.launch(headless=False)
        browser = pw.chromium.launch()
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()
        url = "https://map.kakao.com"

        # Attach the response event listener
        page.on("response", handle_response)

        page.goto(url)  # go to url
        page.reload()
        page.wait_for_load_state("networkidle")
        page.fill("input#search\\.keyword\\.query", "음식점")
        page.click("button#search\\.keyword\\.submit")

        if responses:
            last_response = responses[-1]
            try:
                # Get the raw text of the response
                response_text = last_response.text()
                # Extract the JSON part from the JSONP response
                json_data = re.search(r'\((.*)\)', response_text).group(1)

                # Parse the JSON data
                response_json = json.loads(json_data)

                for place in response_json["places"]:
                    id_list.append(place["confirmid"])

                # Pretty print the JSON response
                # print(json.dumps(response_json, indent=4, ensure_ascii=False))
            except Exception as e:
                print(f"Error retrieving or parsing body: {e}")


        detail_item = {}
        for id_str in set(id_list):
            detail_url = "https://place.map.kakao.com/" + id_str
            detail_page = context.new_page()
            detail_page.goto(detail_url)
            detail_page.wait_for_load_state("networkidle")
            review_cnt_element = detail_page.query_selector("div#mArticle strong.total_evaluation span.color_b")
            if review_cnt_element is None:
                continue
            review_cnt = int(review_cnt_element.inner_text())
            if review_cnt > 3:
                while detail_page.locator("div.evaluation_review a.link_more.link_unfold").count() == 0:
                    detail_page.click("div.evaluation_review a.link_more")
                    detail_page.wait_for_timeout(500)

            title = detail_page.query_selector("div#mArticle div.inner_place h2.tit_location").inner_text()
            evaluation_items = detail_page.locator('div.evaluation_review ul.list_evaluation li')
            index = 1
            for evaluation in evaluation_items.element_handles():
                if evaluation.query_selector("div.unit_info div.inner_user span.txt_username") is None:
                    continue
                detail_item['title'] = title
                detail_item['index'] = index
                detail_item['total_cnt'] = review_cnt
                detail_item['username'] = evaluation.query_selector("div.unit_info div.inner_user span.txt_username").inner_text()
                detail_item['star'] = evaluation.query_selector("div.star_info span.ico_star.inner_star").get_attribute("style")
                detail_item['comment'] = evaluation.query_selector("div.comment_info p.txt_comment span").inner_text()
                index += 1

                print(detail_item)
                print("-----" * 10)

            detail_page.close()