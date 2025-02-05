# 250204
# 나를 위한 자동 영화 추천 프로그램
# 1. 영화 리뷰 크롤링 - 개선판

# 영화 크롤링 타겟 사이트
# https://m.kinolights.com/discover/explore
# ['titles, 'reviews'] # movie_review01.csv
# 영화  500개, 리뷰는 50개
# 해당 사이트는 반응형 웹이라 셀레니움으로 자바스크립트를 실행해도 반응하지 않는 부분이 다수 존재한다. 이는 ActionChains을 이용한다.

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time


# 프로그램 지정 전역 변수
OTT_start_num = 6           # OTT 선택 버튼 지정 변수, 버튼 순서 + 1
OTT_range = 4               # OTT 선택 갯수
movie_num = 500             # 크롤링 영화 갯수
review_num = 50             # 크롤링 리뷰 갯수
start_num = 0               # 영화 시작 번호
ErrorFlag = 0


# 웹 드라이버 세팅
options = ChromeOptions()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'  # 유저 에이전트
options.add_argument('user_agent=' + user_agent)
options.add_argument('lang=ko_KR')
options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 1})  # 알림창 막아준다.
# options.add_argument('--blink-settings=imagesEnabled=false')    # 이미지 로딩을 막아준다.
# options.add_argument('--headless')                              # 헤드리스 모드 활성화
# options.add_argument('--disable-gpu')                           # GPU 비활성화
# options.add_argument('--no-sandbox')                            # 리눅스에서 셀레니움 실행 시 필요할 수 있음

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.set_window_size(1920, 1080)  # 노트북용, 노트북 배율이 다르면 버튼이 안보이는 문제가 있음, 헤드리스 모드 활성화시 같이 활성화


# OTT 선택 버튼을 누르는 함수
def OTTselect(OTT_start, OTT_num):
    try:
        for i in range(OTT_start, (OTT_start + OTT_num)):
            button = driver.find_element(By.XPATH, '//*[@id="contents"]/section/div[2]/div/div/div/div[{}]/button'.format(i))

            # 마우스 커서를 직접 생성해서 클릭 => 반응형 웹이라 자바스크립트를 이용한 클릭은 안됨
            actions = ActionChains(driver)                              # ActionChains으로 마우스 커서 생성
            actions.move_to_element(button).perform()                   # 마우스 커서를 생성 후 해당 요소 위로 이동
            time.sleep(0.1)                                             # 0.1초 대기
            actions.move_to_element(button).click().perform()           # 마우스 커서로 해당 요소 클릭
    except:
        print("An error occurred : OTT_select_error!")
        exit()


# URL 접속 함수, idx = 영화 번호
def siteRefresh(OTT_start, OTT_num, idx):
    try:
        # 방문할 URL
        url = 'https://m.kinolights.com/discover/explore'
        driver.get(url)

        # OTT 선택
        OTTselect(OTT_start, OTT_num)
        time.sleep(0.1)

        # ActionChains 활성화
        actions = ActionChains(driver)          # ActionChains으로 마우스 커서 생성

        # 만약 idx번째 영화에서 에러가 났으면 해당 위치로 이동
        if idx > 0:
            for i in range(int((idx / 4) * 7)):  # 스크롤 횟수를 정수로 바꾸기 위해 int() 사용
                actions.send_keys(Keys.ARROW_DOWN).perform()
                time.sleep(0.05)
    except:
        print("An error occurred : site_refresh_failed! idx : {}".format(idx))
        exit()



# 리뷰 페이지로 이동해서 1편의 영화 리뷰 50개 저장
def crawReviewSave(idx, review_range):
    # 비어있는 리스트 생성 / 영화 단위로 추가
    movies = []
    reviews = []

    # 리뷰 페이지 이동 완료시 CSV 생성
    try:
        # ActionChains 활성화
        actions = ActionChains(driver)
        actions.send_keys(Keys.PAGE_DOWN).perform()        # 페이지 스크롤

        # 해당 페이지를 스크롤 하려면 페이지 다운 버튼을 눌러야 하는데 하나의 방지턱이 존재한다.
        # 이를 리뷰 분류 버튼 중, 전체 버튼을 누르면 아래까지 스크롤 다운이 가능하다.
        # 리뷰 분류 - 전체 클릭
        category_btn_xpath = '//*[@id="contents"]/div[5]/section[2]/div/div[2]/div[1]/button[1]'
        time.sleep(0.3)
        driver.find_element(By.XPATH, category_btn_xpath).click()

        for i in range(100):            # 페이지 아래로 이동해서 리뷰 로딩
            actions.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(0.05)

        # bs4를 이용해서 제목을 추출하기 위해 html 파싱
        resp = driver.page_source                               # 현재 페이지의 HTML을 가져온다.
        soup = BeautifulSoup(resp, 'html.parser')       # bs4를 이용해 파싱
        articles = soup.find_all('article')                     # 'article'이란 태그를 찾아서 리스트로 만든다.

        for article_idx, article in enumerate(articles):        # enumerate로 인덱스와 article을 함께 추출
            try:
                # 최대 50개 리뷰 저장
                if article_idx > (review_range - 1):
                    break                                       # 50개가 넘으면 루프를 종료

                # 리뷰 내용 추출
                # <div data-v-c94717f0="" class="review-item__contents"><a data-v-c194a962="" data-v-c94717f0="" href="/review/287622" data-component-id="reviewList" class="contents__title"><h5 data-v-c94717f0="" data-v-c194a962="">OST 너무 좋아
                # .find()를 이용해서 특정 택스트를 찾는다
                review_element = article.find('div', class_='review-item__contents')    # 리뷰 클래스가 있는 div를 찾아 리스트로 만든다

                if review_element:
                    review = review_element.find('h5').get_text().strip()               # 실제 리뷰 텍스트 추출
                else:
                    review = ''                                                         # Nan값 저장

                # 영화 이름 추출
                movie_xpath = '//*[@id="contents"]/div[1]/div[2]/div[1]/div[1]/h2'
                movie = driver.find_element(By.XPATH, movie_xpath).text

                # 리뷰 저장 메시지 출력
                print(f"{(idx + 1)}번째 영화 : {movie}의 {article_idx}번째 리뷰 저장")
                print(f"리뷰: {review}")

                # 영화와 리뷰 저장
                movies.append(movie)
                reviews.append(review)
            except Exception as e:
                print(f"An error occurred: {e}")
                continue

        # 저장된 리뷰가 50개면
        if len(reviews) == review_range:
            # DataFrame 생성 및 저장
            df_section_movies = pd.DataFrame(movies, columns=['movies'])
            df_section_reviews = pd.DataFrame(reviews, columns=['reviews'])
            df_movies = pd.concat([df_section_movies, df_section_reviews], join='outer', axis=1, ignore_index=False)
            df_movies.to_csv('./crawling_data/movie_reviews_500_movies/movie_review{}.csv'.format(str(idx).zfill(3)))
    except:
        print("An error occurred : review_save_failed! idx : {}".format(idx))

    # 뒤로가기, 홈페이지 설정상 뒤로가도 OTT 선택이 초기화 되지 않는다.
    driver.back()
    time.sleep(0.5)


# 영화 선택 버튼 누르기
def selectMovie(idx):
    try:
        movie_idx = idx + 1
        actions = ActionChains(driver)                              # ActionChains으로 마우스 커서 생성

        # 메뉴 스크롤
        if movie_idx % 4 == 0:
            for i in range(7):  # 스크롤 횟수를 정수로 바꾸기 위해 int() 사용
                actions.send_keys(Keys.ARROW_DOWN).perform()
                time.sleep(0.05)

        # 영화 버튼 누르기
        time.sleep(0.5)  # 0.5초 페이지 로딩
        movie_btn_xpath = driver.find_element(By.XPATH, '//*[@id="contents"]/div/div/div[3]/div[2]/div[{}]/a/div/div[1]/div[1]/img'.format(movie_idx))
        actions.move_to_element(movie_btn_xpath).perform()          # 마우스 커서를 생성 후 해당 요소 위로 이동
        time.sleep(0.1)                                             # 0.1초 대기
        actions.move_to_element(movie_btn_xpath).click().perform()  # 마우스 커서로 해당 요소 클릭
    except:
        print("An error occurred : movie_select_failed! idx : {}".format(idx))
        global ErrorFlag
        ErrorFlag = 1


# 리뷰 페이지 버튼 누르기
def selectReview(idx):
    try:
        # 리뷰 페이지로 이동
        time.sleep(0.5)
        review_btn_xpath = '//*[@id="review"]'
        time.sleep(0.1)
        driver.find_element(By.XPATH, review_btn_xpath).click()
    except:
        try:
            # 버튼이 안보이는 상황 일 수 있으니 아래로 스크롤
            actions = ActionChains(driver)
            for i in range(7):
                actions.send_keys(Keys.ARROW_DOWN).perform()
                time.sleep(0.05)
            selectMovie(idx)
        except:
            try:
                # 버튼이 안보이는 상황 일 수 있으니 위로 스크롤
                actions = ActionChains(driver)
                for i in range(14):
                    actions.send_keys(Keys.ARROW_UP).perform()
                    time.sleep(0.05)
                selectMovie(idx)
            except:
                print("An error occurred : review_select_failed! idx : {}".format(idx))
                global ErrorFlag
                ErrorFlag = 1



def main():
    global ErrorFlag
    siteRefresh(OTT_start_num, OTT_range, start_num)

    for i in range(start_num, movie_num):

        selectMovie(i)
        selectReview(i)
        crawReviewSave(i, review_num)

        if ErrorFlag == 1:
            siteRefresh(OTT_start_num, OTT_range, i)
            ErrorFlag = 0
    print("crawling_complete!")


if __name__ == "__main__":
    main()

