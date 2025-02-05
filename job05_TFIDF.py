# 250204
# 나를 위한 자동 영화 추천 프로그램
# 5. 데이터 벡터화 및 pickle로 저장

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.io import mmwrite, mmread
import pickle


df_reviews = pd.read_csv('./crawling_data/cleaned_reviews.csv')
df_reviews.info()

Tfidf = TfidfVectorizer(sublinear_tf= True)
Tfidf_matrix = Tfidf.fit_transform(df_reviews.reviews)
print(Tfidf_matrix.shape)

with open('./models/tfidf.pickle', 'wb') as f:
    pickle.dump(Tfidf, f)

mmwrite('./models/Tfidf_movie_review.mtx', Tfidf_matrix)

