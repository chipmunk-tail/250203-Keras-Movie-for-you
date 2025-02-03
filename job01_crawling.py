# 250203
# 나를 위한 자동 영화 추천 프로그램
# 1. 영화 리뷰 크롤링

# 영화 크롤링 타겟 사이트
# https://m.kinolights.com/discover/explore
# [제목, 리뷰] # movie_review01.csv
# 영화 1,000개, 게인당 넉넉하게 500개, 리뷰는 50개

# from requests import options
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


# 웹 드라이버 세팅
options = ChromeOptions()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'      # 유저 에이전트
options.add_argument('user_agent=' + user_agent)
options.add_argument('lang=ko_KR')

# options.add_argument('--headless')          # 헤드리스 모드 활성화
# options.add_argument('--disable-gpu')       # GPU 비활성화
# options.add_argument('--no-sandbox')        # 리눅스에서 셀레니움 실행 시 필요할 수 있음


# 알림창 안뜨게 하는 코드
options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 1})

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service = service, options = options)


# 비어있는 데이터 프레임 생성
df_movies = pd.DataFrame()


# 방문할 URL
url = 'https://m.kinolights.com/discover/explore'
driver.get(url)


# OTT 선택 버튼
for i in range(6,10):           # 2부터 시작

    # OTT 선택 버튼 XPath
    # //*[@id="contents"]/section/div[2]/div/div/div/div[2]/button/i    # 넷플릭스
    # //*[@id="contents"]/section/div[2]/div/div/div/div[3]/button/i    # 티빙
    # //*[@id="contents"]/section/div[2]/div/div/div/div[4]/button/i    # 쿠팡 플레이

    button = driver.find_element(By.XPATH, '//*[@id="contents"]/section/div[2]/div/div/div/div[{}]/button'.format(i))

    # 마우스 커서를 직접 생성해서 클릭 => 반응형 웹이라 자바스크립트를 이용한 클릭은 안됨
    actions = ActionChains(driver)                              # ActionChains으로 마우스 커서 생성
    actions.move_to_element(button).perform()                   # 마우스 커서를 생성 후 해당 요소 위로 이동
    time.sleep(0.1)                                             # 0.1초 대기
    actions.move_to_element(button).click().perform()           # 마우스 커서로 해당 요소 클릭




for i in range(1,11):        # 크롤링 하려는 영화 갯수, 1 ~ 500까지

    # 비어있는 리스트 생성 / 영화 단위로 추가
    movies = []
    reviews = []

    # 영화 선택 버튼 XPath
    # //*[@id="contents"]/div/div/div[3]/div[2]/div[1]/a/div/div[1]/div[1]/img      # 웬즈데이
    # //*[@id="contents"]/div/div/div[3]/div[2]/div[2]/a/div/div[1]/div[1]/img      # 중증외상센터
    # //*[@id="contents"]/div/div/div[3]/div[2]/div[3]/a/div/div[1]/div[1]/img      # 말할 수 없는 비밀

    # 영화 선택
    movie_btn_xpath = driver.find_element(By.XPATH, '//*[@id="contents"]/div/div/div[3]/div[2]/div[{}]/a/div/div[1]/div[1]/img'.format(i))
    actions = ActionChains(driver)                                  # ActionChains으로 마우스 커서 생성
    actions.move_to_element(movie_btn_xpath).perform()              # 마우스 커서를 생성 후 해당 요소 위로 이동
    time.sleep(0.2)                                                 # 0.1초 대기
    actions.move_to_element(movie_btn_xpath).click().perform()      # 마우스 커서로 해당 요소 클릭

    # 페이지 전환 기다리는 시간
    time.sleep(1)

    # 리뷰 탭으로 이동
    review_btn_xpath = '//*[@id="review"]'
    time.sleep(1)
    driver.find_element(By.XPATH, review_btn_xpath).click()

    # 페이지 스크롤
    actions.send_keys(Keys.PAGE_DOWN).perform()

    # 해당 페이지를 스크롤 하려면 페이지 다운 버튼을 눌러야 하는데 하나의 방지턱이 존재한다.
    # 이를 리뷰 분류 버튼 중, 전체 버튼을 누르면 아래까지 스크롤 다운이 가능하다.
    # 리뷰 분류 - 전체 클릭
    category_btn_xpath = '//*[@id="contents"]/div[5]/section[2]/div/div[2]/div[1]/button[1]'
    time.sleep(0.3)
    driver.find_element(By.XPATH, category_btn_xpath).click()

    for j in range(100):            # 페이지 아래로 이동해서 리뷰 로딩
        actions.send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(0.05)

    # bs4를 이용해서 제목을 추출하기 위해 html 파싱
    resp = driver.page_source                               # 현재 페이지의 HTML을 가져온다.
    soup = BeautifulSoup(resp, 'html.parser')       # bs4를 이용해 파싱
    articles = soup.find_all('article')                     # 'article'이란 태그를 찾아서 리스트로 만든다.

    # 리뷰 XPath
    # //*[@id="contents"]/div[4]/section[2]/div/article[1]/div[3]/a/h5
    # //*[@id="contents"]/div[4]/section[2]/div/article[2]/div[3]/a[1]/h5   # 더보기 존재
    # //*[@id="contents"]/div[4]/section[2]/div/article[3]/div[3]/a/h5

    for idx, article in enumerate(articles):                # enumerate로 인덱스와 article을 함께 추출
        try:
            # 최대 50개 리뷰 저장
            if idx > 50:
                break  # 50개가 넘으면 루프를 종료

            # 리뷰 내용 추출
            # <div data-v-c94717f0="" class="review-item__contents"><a data-v-c194a962="" data-v-c94717f0="" href="/review/287622" data-component-id="reviewList" class="contents__title"><h5 data-v-c94717f0="" data-v-c194a962="">OST 너무 좋아
            # .find()를 이용해서 특정 택스트를 찾는다
            review_element = article.find('div', class_='review-item__contents')    # 리뷰 클래스가 있는 div를 찾아 리스트로 만든다

            if review_element:
                review = review_element.find('h5').get_text().strip()               # 실제 리뷰 텍스트 추출
            else:
                review = 'No review text available'

            # 영화 이름 추출
            movie_xpath = '//*[@id="contents"]/div[1]/div[2]/div[1]/div[1]/h2'
            movie = driver.find_element(By.XPATH, movie_xpath).text

            # 리뷰 저장 메시지 출력
            print(f"{i}번째 영화 : {movie}의 {idx}번째 리뷰 저장")
            print(f"리뷰: {review}")

            # 영화와 리뷰 저장
            movies.append(movie)
            reviews.append(review)

        except Exception as e:
            print(f"오류 발생: {e}")
            continue

        time.sleep(0.05)

    # DataFrame 생성 및 저장
    df_section_movies = pd.DataFrame(movies, columns=['movies'])
    df_section_reviews = pd.DataFrame(reviews, columns=['reviews'])
    df_temp = pd.concat([df_section_movies, df_section_reviews], join='outer', axis=1, ignore_index=True)
    df_movies = pd.concat([df_movies, df_temp], ignore_index=True)


    # 뒤로가기, 홈페이지 설정상 뒤로가도 OTT 선택이 초기화 되지 않는다.
    driver.back()
    time.sleep(0.5)


    if i % 4 == 0:
        for j in range(7):  # 페이지 아래로 이동해서 영화 로딩    130 * 4 = 체인소맨
            actions.send_keys(Keys.ARROW_DOWN).perform()
            time.sleep(0.05)

    if i % 10 == 0:
        for j in range(4):  # 페이지 아래로 이동해서 영화 로딩    130 * 4 = 체인소맨
            actions.send_keys(Keys.ARROW_DOWN).perform()
            time.sleep(0.05)


# 크롤링이 다 끝났을 경우
driver.close()  # close browser

print(df_movies.head())
df_movies.info()
df_movies.to_csv('./crawling_data/movie_review02.csv')






# article 구조
#
# <html>
#   <body>
#     <article>
#       <h2>영화 1</h2>
#       <p>리뷰 1 내용</p>
#     </article>
#     <article>
#       <h2>영화 2</h2>
#       <p>리뷰 2 내용</p>
#     </article>
#   </body>
# </html>

# [
#     <article>
#       <h2>영화 1</h2>
#       <p>리뷰 1 내용</p>
#     </article>,
#     <article>
#       <h2>영화 2</h2>
#       <p>리뷰 2 내용</p>
#     </article>
# ]

# enumerate
# List = [Apple, Banana, Cherry]
# for idx, List in enumerate(List):
#   print(idx, List)
#
# 0 Apple
# 1 Banana
# 2 Cherry


