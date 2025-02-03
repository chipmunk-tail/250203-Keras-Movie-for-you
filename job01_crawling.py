# 250203
# 나를 위한 자동 영화 추천 프로그램
# 1. 영화 리뷰 크롤링

# 영화 크롤링 타겟 사이트
# https://m.kinolights.com/discover/explore
# 제목, 리뷰
# movie_review01.csv
# 리뷰 있는걸로 1,000개, 게인당 넉넉하게 500개, 리뷰는 50개

from requests import options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd
import time


# Web driver setting
options = ChromeOptions()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
options.add_argument('user_agent=' + user_agent)
options.add_argument('lang=ko_KR')

# 알림창 안뜨게 하는 코드
options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 1})

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service = service, options = options)

# Create empty DataFrame
df_movies = pd.DataFrame()


#
url = 'https://m.kinolights.com/discover/explore'
driver.get(url)

# OTT 선택 버튼 XPath
# //*[@id="contents"]/section/div[2]/div/div/div/div[2]/button/i    # 넷플릭스
# //*[@id="contents"]/section/div[2]/div/div/div/div[3]/button/i    # 티빙
# //*[@id="contents"]/section/div[2]/div/div/div/div[4]/button/i    # 쿠팡 플레이

# OTT select
for i in range(1,5):        # 1, 2, 3, 4
    x = i + 5               # 5, 6, 7, 8

    button = driver.find_element(By.XPATH, '//*[@id="contents"]/section/div[2]/div/div/div/div[{}]/button'.format(x))

    actions = ActionChains(driver)                              # ActionChains으로 마우스 커서 생성
    actions.move_to_element(button).perform()                   # 마우스 커서를 생성 후 해당 요소 위로 이동
    time.sleep(0.3)                                             # 0.3초 대기
    actions.move_to_element(button).click().perform()           # 마우스 커서로 해당 요소 클릭


# 영화 선택 버튼 XPath
# //*[@id="contents"]/div/div/div[3]/div[2]/div[1]/a/div/div[1]/div[1]/img      # 웬즈데이
# //*[@id="contents"]/div/div/div[3]/div[2]/div[2]/a/div/div[1]/div[1]/img      # 중증외상센터
# //*[@id="contents"]/div/div/div[3]/div[2]/div[3]/a/div/div[1]/div[1]/img      # 말할 수 없는 비밀
# //*[@id="contents"]/div/div/div[3]/div[2]/div[4]/a/div/div[1]/div[1]/img      # 스터디그룹
# //*[@id="contents"]/div/div/div[3]/div[2]/div[5]/a/div/div[1]/div[1]/img      # 나의 완벽한 비서

for i in range(1,501):        # 1 ~ 500까지

    # Create empty List
    movies = []
    reviews = []

    # 영화 선택
    # 해당 버튼은 XPath.click()로 누를 수 없기에 직접 마우스 커서를 인식시켜줘야한다.
    movie_btn_xpath = driver.find_element(By.XPATH, '//*[@id="contents"]/div/div/div[3]/div[2]/div[{}]/a/div/div[1]/div[1]/img'.format(i))
    actions = ActionChains(driver)                                  # ActionChains으로 마우스 커서 생성
    actions.move_to_element(movie_btn_xpath).perform()              # 마우스 커서를 생성 후 해당 요소 위로 이동
    time.sleep(0.3)                                                 # 0.3초 대기
    actions.move_to_element(movie_btn_xpath).click().perform()      # 마우스 커서로 해당 요소 클릭

    # 페이지 전환 기다리는 시간
    time.sleep(0.3)

    # 리뷰 탭으로 이동
    review_btn_xpath = '//*[@id="review"]'
    time.sleep(0.3)
    driver.find_element(By.XPATH, review_btn_xpath).click()
    time.sleep(1)

    # 페이지 스크롤
    # 해당 페이지를 스크롤 하려면 페이지 다운 버튼을 눌러야 하는데 하나의 방지턱이 존재한다.
    # 이를 리뷰 분류 버튼 중, 전체 버튼을 누르면 아래까지 스크롤 다운이 가능하다.
    actions.send_keys(Keys.PAGE_DOWN).perform()
    category_btn_xpath = '//*[@id="contents"]/div[5]/section[2]/div/div[2]/div[1]/button[1]'
    time.sleep(0.3)
    driver.find_element(By.XPATH, category_btn_xpath).click()


    # for j in range(400):            # 약 70개 리뷰 로딩
    #     actions.send_keys(Keys.PAGE_DOWN).perform()

    time.sleep(5)


    for j in range(1, 51):

        # 리뷰 XPath
        # //*[@id="contents"]/div[5]/section[2]/div/article[1]/div[3]/a/h5
        # //*[@id="contents"]/div[5]/section[2]/div/article[2]/div[3]/a/h5
        # //*[@id="contents"]/div[4]/section[2]/div/article[1]/div[3]/a/h5
        # //*[@id="contents"]/div[4]/section[2]/div/article[2]/div[3]/a[1]/h5   # 더보기 존재
        # //*[@id="contents"]/div[4]/section[2]/div/article[3]/div[3]/a/h5
        # //*[@id="contents"]/div[4]/section[2]/div/article[10]/div[3]/a/h5
        # //*[@id="contents"]/div[4]/section[2]/div/article[16]/div[3]/a/h5

        # 리뷰 저장

        try:
            review_xpath = '*[@id="contents"]/div[5]/section[2]/div/article[{}]/div[3]/a/h5'.format(j)
            review = driver.find_element(By.XPATH, review_xpath).text
            reviews.append(review)

            # 영화 이름 저장
            movie_xpath = '//*[@id="contents"]/div[1]/div[2]/div[1]/div[1]/h2'
            movie = driver.find_element(By.XPATH, movie_xpath).text
            movies.append(movie)

            print(f"{movie}의 {j}번째 리뷰 저장")

        except:
            movie_xpath = '//*[@id="contents"]/div[1]/div[2]/div[1]/div[1]/h2'
            movie = driver.find_element(By.XPATH, movie_xpath).text
            print(f"{movie}의 리뷰가 없습니다.")
            continue

    # DataFrame 생성 및 저장
    df_section_movies = pd.DataFrame(movies, columns=['movies'])
    df_section_reviews = pd.DataFrame(reviews, columns=['reviews'])
    df_movies = pd.concat([df_movies, df_section_movies, df_section_reviews], axis=1, ignore_index=True)

    # 뒤로가기, 홈페이지 설정상 뒤로가도 OTT 선택이 초기화 되지 않는다.
    driver.back()

    actions.move_by_offset(0, 100).perform()  # (x, y) 오프셋으로 마우스를 이동시킴

# 크롤링이 다 끝났을 경우
driver.close()  # close browser

print(df_movies.head())
df_movies.info()
print(df_movies['reviews'].value_counts())
df_movies.to_csv('./crawling_data/movie_review02.csv')







