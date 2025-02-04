# 250204
# 나를 위한 자동 영화 추천 프로그램
# 2. 크롤링 데이터 합치기_VER.2.0

# 크롤링 코드가 아직 불안정해서 데이터를 따로 받아서 진행

import pandas as pd
import glob

df = pd.read_csv('./crawling_data/movie_400_20250204_combine.csv')
df.dropna(inplace = True)
df.info()
print(df.head())

titles = []
reviews = []
old_title = ''

for i in range(len(df)):
    title = df.iloc[i, 0]
    if title != old_title:
        titles.append(title)
        old_title = title
        df_movie = df[(df.Title == title)]
        review = ' '.join(df_movie.Review)
        reviews.append(review)

print(len(titles))
print(len(reviews))
df = pd.DataFrame({'titles' : titles, 'reviews' : reviews})
df.info()
print(df)

df.to_csv('./crawling_data/reviews_kinolights_1.csv', index = False)