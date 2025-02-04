# 250204
# 나를 위한 자동 영화 추천 프로그램
# 4. 데이터 워드클라우드 출력


import pandas as pd
from matplotlib.pyplot import figure
from wordcloud import WordCloud
import collections
import matplotlib.pyplot as plt
from matplotlib import font_manager

font_path = './format_files/malgun.ttf'
font_name = font_manager.FontProperties(fname = font_path).get_name()
plt.rc('font', family = 'NanumBrunGothic')

df = pd.read_csv('./crawling_data/cleaned_reviews.csv')
words = df.iloc[0, 1].split()               # default = 띄어쓰기 기준으로 잘라줌 => words 에는 형태소가 들어감
print(df.iloc[0, 1])

worddict = collections.Counter(words)
worddict = dict(worddict)
print(worddict)                             # 해당 단어가 몇번 나오는지 딕셔너리 형태로 출력

wordcloud_img = WordCloud(
    background_color = 'white', font_path = font_path).generate_from_frequencies(worddict)
plt.figure(figsize=(12, 12))  # figure 크기 조정
plt.imshow(wordcloud_img, interpolation='bilinear')
plt.axis('off')  # 축을 제거합니다.
plt.show()
