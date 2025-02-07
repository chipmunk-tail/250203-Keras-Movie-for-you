# 250203-Movie-for-you
250203 ~ 250207 intel_AISW

영화 리뷰를 크롤링하여 전처리 후 벡터화하여 선택한 영화와 연관이 높은 영화를 추천하는 프로그램 실습




## 디렉토리 구조

```commandline
250203-Movie-for-you
├─crawling_data
│  ├─movie_reviews_500_movies
│  │  ├─movie_reviews_batch_1.csv
│  │  ├─ ~
│  │  └─movie_reviews_batch_nn.csv
│  ├─cleaned_reviews.csv
│  └─reviews_kinolights.csv
├─format_files
│  ├─malgun.ttf
│  └─stopwords_kor.csv
├─models
│  ├─tfidf.pickle
│  ├─Tfidf_movie_review.mtx
│  └─word2vec_movie_review.model
├─job01_crawling.py
├─job01_1_crawling_improve.py
├─job02_concat.py
├─job02_1_concat.py
├─job03_preprocessing.py
├─job04_word_cloud.py
├─job05_TFIDF.py
├─job06_recommendation.py
├─job06_1_movie_recommendation_app.py
├─job07_word2vec.py
├─job08_word2vec_visuallization.py
├─movie_recommendation.ui
├─README.md
└─requirements.txt
```



## 설명
유사한 문장을 찾는다. ex) 어떤 단어가 몇번 등장하는지에 따라 유사도를 


### job01_crawling.py
키노라이트 모바일 사이트에서 OTT를 선택 후 리뷰를 50개씩 영화 500편을 크롤링 하는 코드


### job01_crawling_improve.py



## 데이터 정규화
- re 패키지로 한글을 제외한 모든 글자를 ' '로 처리
- 불용어 리스트로 불용어 제거
  - 1글자 단어 삭제






### Word 임베딩 실습 사이트
https://word2vec.kr/search/

### 
https://blogs.rstudio.com/ai/posts/2017-12-22-word-embeddings-with-keras/



