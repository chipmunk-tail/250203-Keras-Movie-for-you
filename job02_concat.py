# 250204
# 나를 위한 자동 영화 추천 프로그램
# 2. 크롤링 데이터 합치기

import pandas as pd
import glob

data_path = glob.glob('./crawling_data/movie_reviews_500_movies/*')
print(data_path)

df = pd.DataFrame()

df_temp = pd.read_csv(data_path[0])
print(df_temp.head())

titles = []
reviews = []
old_title = ''

for i in range(len(df_temp)):

    title = df_temp.iloc[i, 0]
    if title != old_title:
        titles.append(title)
        title = old_title
        df_movie = df_temp[(df_temp.movie_title == title)]
        review = ''
        for j in range(len(df_temp)):
            review = review + df_movie.review
            # print(review)
        reviews.append(review)

print(titles[:5])
print(reviews[:5])

