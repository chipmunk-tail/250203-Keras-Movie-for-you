# 250204
# 나를 위한 자동 영화 추천 프로그램
# 3. 데이터 정규화

# job02 로 진행

import pandas as pd
from konlpy.tag import Okt
import re

df = pd.read_csv('./crawling_data/reviews_kinolights.csv')
df. info()

df_stopwords = pd.read_csv('./format_files/stopwords_kor.csv')
stopwords = list(df_stopwords['stopword_kor'])
# print(stopwords)

okt = Okt()
print(df.titles[0])
print(df.reviews[0])

cleand_sentences = []

for review in df.reviews:
    review = re.sub('[^가-힣]', ' ', review)
    print(review)

    tokened_review = okt.pos(review, stem=True)
    print(tokened_review)

    df_token = pd.DataFrame(tokened_review, columns=['word', 'class'])
    df_token = df_token[(df_token['class'] == 'Noun') |
                        (df_token['class'] == 'Verb') |
                        (df_token['class'] == 'Adjective')]
    print(df_token)

    words = []
    for word in df_token.word:
        if 1 < len(word):
            if word not in stopwords:
                words.append(word)
    cleand_sentence = ' '.join(words)
    cleand_sentences.append(cleand_sentence)
    print(cleand_sentences)

df.reviews = cleand_sentences
df.dropna(inplace = True)
df.to_csv('./crawling_data/cleaned_reviews.csv', index = False)