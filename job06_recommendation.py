# 250204
# 나를 위한 자동 영화 추천 프로그램
# 5. 데이터 벡터화 및 pickle로 저장

import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread
import pickle
from konlpy.tag import Okt
from gensim.models import Word2Vec



def getRecommendation(cosine_sim):
    simScore = list(enumerate(cosine_sim[-1]))
    simScore = sorted(simScore, key=lambda x:x[1], reverse=True)
    simScore = simScore[:11]
    movieIdx = [i[0] for i in simScore]
    recmovieList = df_reviews.iloc[movieIdx, 0]
    return recmovieList[1:11]

df_reviews = pd.read_csv('./crawling_data/cleaned_reviews.csv')
Tfidf_matrix = mmread('./models/Tfidf_movie_review.mtx').tocsr()
with open('./models/tfidf.pickle', 'rb') as f:
    Tfidf = pickle.load(f)


# 영화 index 이용
ref_idx = 349
print('title', df_reviews.iloc[ref_idx, 0])
cosine_sim = linear_kernel(Tfidf_matrix[ref_idx], Tfidf_matrix)
print(cosine_sim[0])
print(len(cosine_sim[0]))
recommendations = getRecommendation(cosine_sim)
print(recommendations)


