# coding: utf-8

from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, HTTPServer
from xml.etree import ElementTree

conn = None
server = 'openapi.animal.go.kr'

def connectOpenAPIServer():
    global conn, server
    conn = HTTPConnection(server)

def getAnimalDataFromITEM(item):
    global conn, server, regKey
    if conn == None:
        connectOpenAPIServer()
    uri = 'http://openapi.animal.go.kr/openapi/service/rest/abandonmentPublicSrvc/kind?up_kind_cd=417000&ServiceKey=eVsoaZvhhkQhlgRn%2F%2BHKFZM7Pbob28TY%2BGFE9%2BMgq5qum5e22G0Y85%2F3V36c1EQEAgQr8zoeiyzQDEDazY394w%3D%3D'
    conn.request('GET', uri)

    req = conn.getresponse()
    if int(req.status) == 200:
        print('Animal data downloading complete')
        return req.read()
    else:
        print('OpenAPI requset has been failed! please retry')
        return None

def extractAnimalData(strXml):
    tree = ElementTree.fromstring(strXml)
    AnimalElements = tree.getiterator('item')
    AnimalList = []
    for Animal in AnimalElements:
        item = Animal.find('KNm')
        strCareNm = Animal.find('kindCd')
        if len(strCareNm.text) > 0:
            AnimalList.append({'이름':item.text, '코드':strCareNm.text})
    return AnimalList

if __name__ == '__main__':
    animalXML = getAnimalDataFromITEM(None)
    animalList = extractAnimalData(animalXML)
    print(animalList)