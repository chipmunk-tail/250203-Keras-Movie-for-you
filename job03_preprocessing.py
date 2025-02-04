

import pandas as pd
from konlpy.tag import Okt
import re

from job01_crawling import review

df = pd.read_csv('./crawling_data/reviews_kinolights.csv')
df. info()

df_stopwords = pd.read_csv('./format_files/stopwords_kor.csv')
stopwords = list(df_stopwords['stopword_kor'])
# print(stopwords)

okt = Okt()
print(df.titles[0])
print(df.reviews[0])

review = re.sub('[^가-힣]', ' ', review)
print(review)

tokened_review = okt.pos(review, stem = True)
print(tokened_review)

