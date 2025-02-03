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
    i = i + 4               # 5, 6, 7, 8
    movie_btn_xpath = '//*[@id="contents"]/section/div[2]/div/div/div/div[{}]/button/i'.format((i + 1))
    time.sleep(0.3)
    driver.find_element(By.XPATH, movie_btn_xpath).click()


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
    movie_btn_xpath = '//*[@id="contents"]/div/div/div[3]/div[2]/div[{}]/a/div/div[1]/div[1]/img'.format(i)
    time.sleep(0.3)
    driver.find_element(By.XPATH, movie_btn_xpath).click()

    # 페이지 전환 기다리는 시간
    time.sleep(0.3)

    # 리뷰 탭으로 이동
    movie_btn_xpath = '//*[@id="review"]'
    time.sleep(0.3)
    driver.find_element(By.XPATH, movie_btn_xpath).click()

    # 페이지 스크롤
    driver.execute_script('window.scrollTo(0, 2000)')  # scroll to the bottom of the site to activate button
    time.sleep(0.8)


    for j in range(1, 51):

        # 리뷰 XPath
        # //*[@id="contents"]/div[5]/section[2]/div/article[1]/div[3]/a/h5
        # //*[@id="contents"]/div[5]/section[2]/div/article[2]/div[3]/a/h5

        try:
            #리뷰 저장
            review_xpath = '*[@id="contents"]/div[5]/section[2]/div/article[{}]/div[3]/a/h5'.format(j)
            review = driver.find_element(By.XPATH, review_xpath).text
            reviews.append(review)

            # 영화 이름 저장
            movie_xpath = '//*[@id="contents"]/div[1]/div[2]/div[1]/div[1]/h2'
            movie = driver.find_element(By.XPATH, movie_xpath).text
            movies.append(movie)

        except:
            movie_xpath = '//*[@id="contents"]/div[1]/div[2]/div[1]/div[1]/h2'
            movie = driver.find_element(By.XPATH, movie_xpath).text
            movies.append(movie)
            print(f"{movie}의 리뷰가 없습니다.")
            break

        # 리뷰 로딩을 위해 스크롤
        driver.execute_script('window.scrollTo(0, 100)')    # scroll to the bottom of the site to activate button
        time.sleep(0.3)

    df_section_movies = pd.DataFrame(movies, columns = ['movies'])              # Create columns 'movies'
    df_section_movies['movies'] = movies[i]
    df_section_reviews = pd.DataFrame(reviews, columns = ['reviews'])              # Create columns 'movies'
    df_section_reviews['review'] = reviews[i]
    df_movies = pd.concat([df_movies, df_section_movies, df_section_reviews], axis = 'rows', ignore_index = True)

    # 뒤로가기, 홈페이지 설정상 뒤로가도 OTT 선택이 초기화 되지 않는다.
    driver.back()


# 크롤링이 다 끝났을 경우
driver.close()  # close browser

print(df_movies.head())
df_movies.info()
print(df_movies['reviews'].value_counts())
df_movies.to_csv('./crawling_data/movie_review02.csv')







