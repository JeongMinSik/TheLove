# coding: utf-8

from http.client import HTTPConnection
from xml.etree import ElementTree
from urllib.parse import *


##global
conn = None
server = "api.visitkorea.or.kr"
regKey = 'ru%2FC4Y79jSuHJzxUpPXR9qr%2FF2ZuOwapItcjtHWPt2OJlYET56OMRkZ8i1EsMjOtT5nWR88VqFGCJ3vOOMPRZw%3D%3D'

areaDic = {"전국" : '', "서울" : '1', "인천" : '2', "대전":'3', "대구":'4', "광주":'5', "부산":'6',"울산":'7',"세종특별자치시":'8',"경기도":'31',
           "강원도":'32',"충청북도":'33',"충청남도":'34',"경상북도":'35',"경상남도":'36',"전라북도":'37',"전라남도":'38',"제주도":'39'}
contentDic = {"전체 분류":'',"관광지":'12',"문화시설":'14',"행사/공연/축제":'15',"여행코스":'25',"레포츠":'28',"숙박":'32',"쇼핑":'38',"음식점":'39'}
#수정할거면 아래 전체분류도 수정

def userURIBuilder(server, findType, **user):
    str = "http://" + server + "/openapi/service/rest/KorService/" + findType + "?"
    for key in user.keys():
        if key == 'keyword':
            str += urlencode({key : user[key]}) +'&'
        else:
            str += key + "=" + user[key]+ '&'
    return str

def changeOption(area,content):
    for key in areaDic.keys():
        if key == area:
            area = areaDic[key]
    for key in contentDic.keys():
        if key == content:
            content = contentDic[key]
    return area, content


def getTourDataFromDate(findType, area, date, content='전체 분류',keyword=''):
    global server, regKey, conn

    area, content = changeOption(area,content)
    if conn == None:
        conn = HTTPConnection(server)

    uri = userURIBuilder(server, findType, ServiceKey=regKey, eventStartDate=date, areaCode=area, contentTypeId =content, keyword = keyword,MobileOS='ETC', MobileApp='AppTesting', numOfRows='1000')
    try:
        conn.request("GET", uri)
        req = conn.getresponse()
    except WindowsError as error:
        print(error)
        return None
    #print (req.status)
    if int(req.status) == 200:
        print("Tour data downloading complete!")
        return ElementTree.fromstring(req.read())
    else:
        print ("Tour API request has been failed!! please retry")
        return None


def getLocationData(strX,strY):
    global server, regKey, conn
    if conn == None:
        conn = HTTPConnection(server)
    uri = userURIBuilder(server, 'locationBasedList', ServiceKey=regKey,mapX =strX, mapY = strY, radius = '20000', numOfRows='100', arrange = 'E' , MobileApp='AppTesting',MobileOS='ETC')
    try:
        conn.request("GET", uri)
        req = conn.getresponse()
    except WindowsError as error:
        print(error)
        return None

    locationList = None
    if int(req.status) == 200:
        print("Location data downloading complete!")
        locationList = ElementTree.fromstring(req.read())
    else:
        print ("Location API request has been failed!! please retry")
        return None

    if locationList == None or locationList.find("body").find("totalCount").text == '0':
        return None

    locationList=locationList.getiterator("item")
    restaurant = '-'
    stay = '-'
    for location in locationList:
        try:
            if restaurant == '-' and location.find("contenttypeid").text == contentDic["음식점"]:
                restaurant = location.find("title").text + "("+location.find("dist").text +"m)"
            elif stay == '-' and location.find("contenttypeid").text == contentDic["숙박"]:
                stay = location.find("title").text + "(" + location.find("dist").text + "m)"
            if restaurant != '-' and stay != '-':
                break
        except:
            continue
    return restaurant + "\n" + stay


def getTourInfo(isKeyword, festivalList,date):
    if festivalList == None or festivalList.find("body").find("totalCount").text == '0':
        return None
    # Festival 엘리먼트를 가져옵니다.
    festivalInfo = []
    festivalList = festivalList.getiterator("item")  # return list type

    for festival in festivalList:
        try:
            title = festival.find("title").text
            addr = festival.find("addr1").text
            image =festival.find("firstimage").text
            mapX = festival.find("mapx").text
            mapY = festival.find("mapy").text

            if isKeyword == True:
                contentType = festival.find("contenttypeid").text
                for key in contentDic.keys():
                    if contentType == contentDic[key]:
                        contentType = key
                        break
                festivalInfo.append({"image": image, "title": title, "addr": addr, "eventdate": contentType, "mapX" :mapX, "mapY" :mapY})
            else:
                eventStartdate = festival.find("eventstartdate").text
                eventEnddate = festival.find("eventenddate").text
                if eventStartdate <= date <= eventEnddate:
                    festivalInfo.append({"image": image, "title": title, "addr": addr, "eventdate": eventStartdate + " ~ " + eventEnddate, "mapX" :mapX, "mapY" :mapY})
        except:
            continue
    if len(festivalInfo) > 0:
        return festivalInfo
    else:
        return None