# -*- coding: cp949 -*-
from http.client import HTTPConnection

##global
conn = None
server = "www.kobis.or.kr"
regKey = 'b2469288dbc7cf61d1484f741294e1a5'

def userURIBuilder(server,**user):
    str = "http://" + server + "/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.xml" + "?"
    for key in user.keys():
        str += key + "=" + user[key] + "&"
    return str

def connectOpenAPIServer():
    global conn, server
    conn = HTTPConnection(server)

def getMovieDataFromDate(date):
    global server, regKey, conn
    if conn == None:
        connectOpenAPIServer()
    uri = userURIBuilder(server, key=regKey, targetDt=date)

    conn.request("GET", uri)

    req = conn.getresponse()
    print (req.status)
    if int(req.status) == 200 :
        print("Movie data downloading complete!")
        return extractMovieData(req.read())
    else:
        print ("OpenAPI request has been failed!! please retry")
        return None

def extractMovieData(strXml):
    from xml.etree import ElementTree
    tree = ElementTree.fromstring(strXml)
    print (strXml)
    # Movie 엘리먼트를 가져옵니다.
    itemElements = tree.getiterator("dailyBoxOffice")  # return list type
    print(itemElements)
    for item in itemElements:
        rank = item.find("rank")
        strTitle = item.find("movieNm")
        print (strTitle)
        if len(strTitle.text) > 0 :
           return {"Rank:":rank.text,"Title":strTitle.text}


print(getMovieDataFromDate('20160501'))

