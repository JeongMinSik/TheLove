
# -*- coding: cp949 -*-
from http.client import HTTPConnection
from xml.etree import ElementTree

##global
conn = None
server = "www.kobis.or.kr"
regKey = "ru%2FC4Y79jSuHJzxUpPXR9qr%2FF2ZuOwapItcjtHWPt2OJlYET56OMRkZ8i1EsMjOtT5nWR88VqFGCJ3vOOMPRZw%3D%3D"

weekDic = {"�Ϻ�": '', "�ְ�(��~��)": '0', "�ָ�(��~��)": '1', "����(��~��)": '2'}
multiDic = {"���+�پ缺": '', "�����ȭ": 'N', "�پ缺��ȭ": 'Y'}
nationDic = {"�ѱ�+�ܱ�": '', "�ѱ���ȭ": 'K', "�ܱ���ȭ": 'F'}

def userURIBuilder(server, type, **user):
    type = type.replace(type[0],type[0].upper(),1)
    str = "http://" + server + "/kobisopenapi/webservice/rest/boxoffice/search"+ type +"List.xml" + "?"
    for key in user.keys():
        str += key + "=" + user[key] + "&"
    return str

def changeOption(week,multi,nation):
    for key in weekDic.keys():
        if key == week:
            week = weekDic[key]
            break
    for key in multiDic.keys():
        if key == multi:
            multi = multiDic[key]
            break
    for key in nationDic.keys():
        if key == nation:
            nation = nationDic[key]
            break
    return week,multi,nation

def getMovieDataFromDate(date,type,week,multi,nation):
    global server, regKey, conn
    if conn == None:
        conn = HTTPConnection(server)

    #�ɼǺ���
    week, multi, nation = changeOption(week,multi,nation)
    uri = userURIBuilder(server, type, key=regKey, targetDt=date, weekGb=week, multiMovieYn =multi, repNationCd = nation)
    try:
        conn.request("GET", uri)
        req = conn.getresponse()
    except WindowsError as error:
        print(error)
        return None

    #print (req.status)
    if int(req.status) == 200:
        print("Movie data downloading complete!")
        return ElementTree.fromstring(req.read())
    else:
        print ("Movie API request has been failed!! please retry")
        return None

def getMovieInfo(movieList,type):
    if movieList == None or movieList.find("showRange") == None:
        return None, None

    # �ڽ����ǽ� ������ ���
    boxofficeInfo = "*** " + movieList.find("boxofficeType").text + " [ �Ⱓ: " + movieList.find("showRange").text + " ] ***"
    # Movie ������Ʈ�� �����ɴϴ�.
    moviesInfo = []
    movieList = movieList.getiterator(type)  # return list type
    for movie in movieList:
        rank = movie.find("rank")
        strTitle = movie.find("movieNm")
        strOpenDate = movie.find("openDt")
        audiAcc = movie.find("audiAcc")
        if len(strTitle.text) > 0:
            moviesInfo.append({"rank":rank.text, "movieNm":strTitle.text, "openDt":strOpenDate.text, "audiAcc":audiAcc.text})
    if len(moviesInfo) > 0:
        return (boxofficeInfo,moviesInfo)
    else:
        return None, None

def findYesterday():
    from datetime import date
    import time
    yesterday = date.fromtimestamp(time.time()-60*60*24)
    date = str(yesterday.year)
    if yesterday.month < 10:
        date += '0'
    date += str(yesterday.month)
    if yesterday.day < 10:
        date += '0'
    date += str(yesterday.day)
    return date
