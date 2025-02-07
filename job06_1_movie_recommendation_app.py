

import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from gensim.models import Word2Vec
from scipy.io import mmread
import pickle
from PyQt5.QtCore import QStringListModel
from PyQt5.QtCore import Qt


from_window = uic.loadUiType('./movie_recommendation.ui')[0]


class Exam(QWidget, from_window):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Tfidf_matrix = mmread('./models/Tfidf_movie_review.mtx').tocsr()
        with open('./models/tfidf.pickle', 'rb') as f:
            self.Tfidf = pickle.load(f)

        self.df_reviews = pd.read_csv('./crawling_data/cleaned_reviews.csv')
        self.titles = list(self.df_reviews.titles)
        self.titles.sort()
        # self.cb_title.addItem('Test01')
        for title in self.titles:
            self.cb_title.addItem(title)

        self.cb_title.currentIndexChanged.connect(self.combobox_slot)

    def combobox_slot(self):
        title = self.cb_title.currentText()
        print(title)
        recommendation = self.recommendation_by_title(title)
        self.lbl_recommendation.setText(recommendation)


    def recommendation_by_title(self, title):
        movie_idx = self.df_reviews[self.df_reviews.titles == title].index[0]
        cosine_sim = linear_kernel(self.Tfidf_matrix[movie_idx], self.Tfidf_matrix)
        recommendation = self.getRecommendation(cosine_sim)
        recommendation = '\n'.join(list(recommendation))
        return recommendation

    def getRecommendation(self, cosine_sim):
        simScore = list(enumerate(cosine_sim[-1]))
        simScore = sorted(simScore, key=lambda x: x[1], reverse=True)
        simScore = simScore[:11]
        movieIdx = [i[0] for i in simScore]
        recmovieList = self.df_reviews.iloc[movieIdx, 0]
        return recmovieList[1:11]


if __name__ == '__main__':

    # 노트북 윈도우 배열 문제
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)     # PyQt가 Windows 배율 설정을 감지하고 조절하도록 함
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)        # 아이콘, 그래픽 요소가 흐려지는 문제 해결

    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())
















