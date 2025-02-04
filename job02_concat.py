# 250204
# 나를 위한 자동 영화 추천 프로그램
# 2. 크롤링 데이터 합치기

# 크롤링 코드가 아직 불안정해서 데이터를 따로 받아서 진행

import pandas as pd
import glob

data_paths = glob.glob('./crawling_data/movie_reviews_500_movies/*')
print(data_paths)

df = pd.DataFrame()

for path in data_paths:
    # 각 파일을 읽어오기
    df_temp = pd.read_csv(path)
    print(df_temp.head())

    titles = []
    reviews = []
    old_title = ''

    for i in range(len(df_temp)):
        title = df_temp.iloc[i, 0]

        # 제목이 이전 제목과 다르면 제목을 추가
        if title != old_title:
            title = title.replace('"', '')  # 제목에서 불필요한 따옴표 제거
            titles.append(title)
            old_title = title

            # 같은 제목을 가진 리뷰들을 하나로 합침
            df_movie = df_temp[df_temp.movie_title == title]
            review = ' '.join(df_movie.review)
            reviews.append(review)

    print(len(titles))
    print(len(reviews))

    # 새로운 데이터프레임 배치 생성
    df_batch = pd.DataFrame({'titles': titles, 'reviews': reviews})
    df_batch.info()
    print(df_batch)

    # 기존 데이터프레임에 새로운 배치 합치기
    df = pd.concat([df, df_batch], ignore_index=True)

df.info()
df.to_csv('./crawling_data/reviews_kinolights.csv', index=False)
