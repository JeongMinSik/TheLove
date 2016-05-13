
# coding: utf-8

import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtNetwork import *
from PyQt5 import uic
from urllib.request import Request, urlopen

from movie import *
from tour import *

##global
movieMAX = 10
festivalMAX = 6

class Form(QDialog):
    def __init__(self, parent=None):
        from datetime import date
        import time

        QDialog.__init__(self, parent)
        self.ui = uic.loadUi("ui.ui",self)
        self.ui.setWindowIcon(QIcon('heart.ico'))
        self.ui.dateEdit_Movie.setDate(date.fromtimestamp(time.time()-60*60*24)) #어제
        self.ui.dateEdit_Tour.setDate(date.today())

        self.ui.checkBox_keyword.toggle()
        #self.ui.checkBox_festival.toggle()

        #함수 연결
        self.ui.checkBox_keyword.stateChanged.connect(self.changeKeyword)
        self.ui.checkBox_festival.stateChanged.connect(self.changeFestival)

        self.ui.movieButton.toggled.connect(self.setOffMovieButton)
        self.ui.movieButton.clicked.connect(self.showMovieData)

        self.ui.tourButton.toggled.connect(self.setOffTourButton)
        self.ui.tourButton.clicked.connect(self.showTourData)

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
                             [self.ui.imageF_4, self.ui.titleF_4, self.ui.addrF_4, self.ui.startend_4, self.ui.weather_4],
                             [self.ui.imageF_5, self.ui.titleF_5, self.ui.addrF_5, self.ui.startend_5, self.ui.weather_5]
                            ]

    def changeKeyword(self,state):
        if state == Qt.Checked:
            self.ui.checkBox_festival.setCheckState(Qt.Unchecked)
            self.ui.ComboBox_content.setEnabled(True)
            self.ui.lineEdit_keyword.setEnabled(True)
        else:
            self.ui.checkBox_festival.setCheckState(Qt.Checked)
            self.ui.ComboBox_content.setEnabled(False)
            self.ui.lineEdit_keyword.setEnabled(False)

    def changeFestival(self, state):
        if state == Qt.Checked:
            self.ui.checkBox_keyword.setCheckState(Qt.Unchecked)
        else:
            self.ui.checkBox_keyword.setCheckState(Qt.Checked)

    def setOffMovieButton(self):
        print("토글함수진입1")
        self.ui.movieButton.setText("검색 중...")
        self.ui.movieButton.setEnabled(False)
    def setOffTourButton(self):
        print("토글함수진입2")
        self.ui.tourButton.setText("검색 중...")
        self.ui.tourButton.setEnabled(False)
    def setOnButton(self, button):
        print("함수진입3")
        button.setText("검색")
        button.setEnabled(True)

    # errorType = 0 영화, 1 행사
    def error(self,errorType,keyword):
        QMessageBox.warning(self, "Error", "[ " + keyword + " ] \n위 조건에 맞는 데이터가 없습니다.")

        # 빈칸 초기화
        if errorType == 0:
            for i in range(0, movieMAX):
                self.movieArr[i][0].setText('-')
                self.movieArr[i][1].setText('-')
                self.movieArr[i][2].setText('-')
                self.movieArr[i][3].setText('-')
        elif errorType == 1:
            for i in range(0, festivalMAX):
                self.festivalArr[i][0].setText('-')
                self.festivalArr[i][1].setText('-')
                self.festivalArr[i][2].setText('-')
                self.festivalArr[i][3].setText('-')


    # 영화데이터 불러오기
    def showMovieData(self):
        print("영화데이터진입")
        #옵션값
        type_txt = self.ui.mComboBox_type.currentText()
        multi_txt = self.ui.mComboBox_multi.currentText()
        nation_txt = self.ui.mComboBox_nation.currentText()

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

        type = None
        if type_txt == '일별':
            type = 'dailyBoxOffice'
        else:
            type = 'weeklyBoxOffice'
        movieList = getMovieDataFromDate(strDate,type,type_txt,multi_txt,nation_txt)
        info, list = getMovieInfo(movieList,type)

        if info==None:
            self.setOnButton(self.ui.movieButton)
            self.error(0,"구분:" + type_txt + ", 날짜:"+ str(date.year()) + "년 " + str(date.month()) +"월 "+ str(date.day()) + "일")
            return

        # 영화정보 설정
        y=0
        for movie in list:
            self.movieArr[y][0].setText(movie['rank'])
            self.movieArr[y][1].setText(movie['movieNm'])
            self.movieArr[y][2].setText(movie['openDt'])
            self.movieArr[y][3].setText(movie['audiAcc'])
            y+=1

        # 결과창
        self.setOnButton(self.ui.movieButton)
        QMessageBox.information(self, "Info", info + "\n \t  조회가 완료되었습니다!")

    #여행 데이터 불러오기
    def showTourData(self):
        # 옵션값 불러오기
        area_txt = self.ui.ComboBox_area.currentText()
        content_txt = self.ui.ComboBox_content.currentText()
        keyword_txt = self.ui.lineEdit_keyword.text()

        # 날짜 불러오기
        date = self.ui.dateEdit_Tour.date()
        strDate = ''
        strDate += str(date.year())
        if date.month() < 10:
            strDate += '0'
        strDate += str(date.month())
        if date.day() < 10:
            strDate += '0'
        strDate += str(date.day())

        TourInfo = None

        #키워드검색
        if self.ui.checkBox_keyword.isChecked() == True:
            FestivalList = getTourDataFromDate('searchKeyword', area_txt, strDate,content_txt, keyword_txt)
            TourInfo = getTourInfo(True,FestivalList,strDate)
            if TourInfo == None:
                self.setOnButton(self.ui.tourButton)
                self.error(1, "지역:" + area_txt + ", 분류:" + content_txt +", 키워드:'" + keyword_txt + "'")
                return
        #행사검색
        else:
            FestivalList = getTourDataFromDate('searchFestival',area_txt,strDate)
            TourInfo = getTourInfo(False,FestivalList,strDate)
            if TourInfo == None:
                self.setOnButton(self.ui.tourButton)
                self.error(1, "지역:" + area_txt + ", 날짜:"+ str(date.year()) + "년 " + str(date.month()) +"월 "+ str(date.day()) + "일")
                return

        #여행정보 설정
        y=0
        buffer = QPixmap()
        for festival in TourInfo:
            #이미지보여주기
            req = Request(festival['image'], headers={'User-Agent': 'Mozilla/5.0'})
            data = urlopen(req).read()
            buffer.loadFromData(data)
            self.festivalArr[y][0].setPixmap(buffer.scaled(self.festivalArr[y][0].size()))
            #self.festivalArr[y][0].move(0, 0)
            self.festivalArr[y][0].show()

            self.festivalArr[y][1].setText(festival['title'])
            self.festivalArr[y][2].setText(festival['addr'])
            self.festivalArr[y][3].setText(festival['eventdate'])
            y += 1
            if y == festivalMAX:
                break
        if y != festivalMAX:
            for i in range(y,festivalMAX):
                self.festivalArr[i][0].setText('-')
                self.festivalArr[i][1].setText('-')
                self.festivalArr[i][2].setText('-')
                self.festivalArr[i][3].setText('-')

        # 결과창
        self.setOnButton(self.ui.tourButton)
        QMessageBox.information(self, "Info", "\n 데이트정보 조회가 완료되었습니다!")

if __name__ == '__main__':
    while(True):
        app = QApplication(sys.argv)
        f = Form()
        sys.exit(app.exec())
