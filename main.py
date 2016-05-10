
# coding: utf-8
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

from movie import *
from Tour import *

class Form(QtWidgets.QDialog):
    def __init__(self, parent=None):
        # 최대개수
        self.movieMAX = 10
        self.festivalMAX = 4

        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi("ui.ui",self)
        self.ui.setWindowTitle("TheLove")
        self.ui.setWindowIcon(QIcon('heart.png'))
        self.ui.show()
        self.movieArr= [ [self.ui.rank_0, self.ui.movieNm_0, self.ui.openDt_0,self.ui.audiAcc_0],
                         [self.ui.rank_1, self.ui.movieNm_1, self.ui.openDt_1, self.ui.audiAcc_1],
                         [self.ui.rank_2, self.ui.movieNm_2, self.ui.openDt_2, self.ui.audiAcc_2],
                         [self.ui.rank_3, self.ui.movieNm_3, self.ui.openDt_3, self.ui.audiAcc_3],
                         [self.ui.rank_4, self.ui.movieNm_4, self.ui.openDt_4, self.ui.audiAcc_4],
                         [self.ui.rank_5, self.ui.movieNm_5, self.ui.openDt_5, self.ui.audiAcc_5],
                         [self.ui.rank_6, self.ui.movieNm_6, self.ui.openDt_6, self.ui.audiAcc_6],
                         [self.ui.rank_7, self.ui.movieNm_7, self.ui.openDt_7, self.ui.audiAcc_7],
                         [self.ui.rank_8, self.ui.movieNm_8, self.ui.openDt_8, self.ui.audiAcc_8],
                         [self.ui.rank_9, self.ui.movieNm_9, self.ui.openDt_9, self.ui.audiAcc_9],
                        ]
        self.festivalArr = [ [self.ui.imageF_0, self.ui.titleF_0, self.ui.addrF_0, self.ui.startend_0, self.ui.weather_0],
                             [self.ui.imageF_1, self.ui.titleF_1, self.ui.addrF_1, self.ui.startend_1, self.ui.weather_1],
                             [self.ui.imageF_2, self.ui.titleF_2, self.ui.addrF_2, self.ui.startend_2, self.ui.weather_2],
                             [self.ui.imageF_3, self.ui.titleF_3, self.ui.addrF_3, self.ui.startend_3, self.ui.weather_3],
                            ]

    # type = 0 영화, 1 행사
    def error(self,errorType,keyword):
        QMessageBox.information(self, "Error", "[" + keyword + "]에 관한 데이터가 없습니다.")

        #빈칸 초기화
        if errorType == 0:
            for i in range(0, 10):
                self.movieArr[i][0].setText('-')
                self.movieArr[i][1].setText('-')
                self.movieArr[i][2].setText('-')
                self.movieArr[i][3].setText('-')
        elif errorType == 1:
            for i in range(0, 4):
                self.festivalArr[i][0].setText('-')
                self.festivalArr[i][1].setText('-')
                self.festivalArr[i][2].setText('-')
                self.festivalArr[i][3].setText('-')

    # 영화 데이터 불러오기
    @pyqtSlot()
    def showMovieData(self):
        # 날짜 불러오기
        date = self.ui.dateEdit_Movie.date()
        strDate = ''
        strDate += str(date.year())
        if date.month() < 10:
            strDate += '0'
        strDate += str(date.month())
        if date.day() < 10:
            strDate += '0'
        strDate += str(date.day())

        movieList = getMovieDataFromDate(strDate)
        info, list = getMovieInfo(movieList)

        if info==None:
            self.error(0,strDate)
            return

        # 영화텍스트 설정
        y=0
        for movie in list:
            self.movieArr[y][0].setText(movie['rank'])
            self.movieArr[y][1].setText(movie['movieNm'])
            self.movieArr[y][2].setText(movie['openDt'])
            self.movieArr[y][3].setText(movie['audiAcc'])
            y+=1

        # 결과창
        QMessageBox.information(self, "Info", info + "\n \t  조회가 완료되었습니다!")

    #행사 데이터 불러오기
    @pyqtSlot()
    def showFestivalData(self):
        # 날짜 불러오기
        date = self.ui.dateEdit_Festival.date()
        strDate = ''
        strDate += str(date.year())
        if date.month() < 10:
            strDate += '0'
        strDate += str(date.month())
        if date.day() < 10:
            strDate += '0'
        strDate += str(date.day())

        FestivalList = getFestivalDataFromDate(strDate)
        FestivalInfo = getFestivalInfo(FestivalList)

        if FestivalInfo == None:
            self.error(1, strDate)
            return

        #축제 텍스트 설정
        y=0
        for festival in FestivalInfo:
            self.festivalArr[y][0].setText(festival['image'])
            self.festivalArr[y][1].setText(festival['title'])
            self.festivalArr[y][2].setText(festival['addr'])
            self.festivalArr[y][3].setText(festival['eventdate'])
            y+=1
            if y == 4:
                break
        if y != 4:
            for i in range(y,4):
                self.festivalArr[i][0].setText('-')
                self.festivalArr[i][1].setText('-')
                self.festivalArr[i][2].setText('-')
                self.festivalArr[i][3].setText('-')

        # 결과창
        QMessageBox.information(self, "Info", "\n 행사 조회가 완료되었습니다!")

if __name__ == '__main__':
    while(True):
        app = QtWidgets.QApplication(sys.argv)
        w = Form()
        sys.exit(app.exec())
