#from http.client import HTTPConnection

##global
#conn = None
#server = "api.visitkorea.or.kr"

#conn = HTTPConnection(server)
#conn.request("GET", "/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.xml?repNationCd=&targetDt=20160518&key=b2469288dbc7cf61d1484f741294e1a5&weekGb=&multiMovieYn=&")

# smtp 정보
#host = "smtp.gmail.com" # Gmail SMTP 서버 주소.
port = "587"

def MakeHtmlDoc(movieList,tourList):
    from xml.dom.minidom import getDOMImplementation
    #get Dom Implementation
    impl = getDOMImplementation()

    newdoc = impl.createDocument(None, "html", None)  #DOM 객체 생성
    top_element = newdoc.documentElement
    header = newdoc.createElement('header')
    top_element.appendChild(header)
    # Body 엘리먼트 생성.
    body = newdoc.createElement('body')

    if movieList != None:
        body.appendChild(newdoc.createTextNode("==================== 박스 오피스 ===================="))
        body.appendChild(newdoc.createElement('br'))
        body.appendChild(newdoc.createElement('br'))
        for item in movieList:
            # BR 태그 (엘리먼트) 생성.
            br = newdoc.createElement('br')
            #create bold element
            p = newdoc.createElement('p')
            #create text node
            p.appendChild(newdoc.createTextNode("순위:" + item['rank'] + "     "))
            p.appendChild(newdoc.createTextNode("제목:" + item['movieNm'] + "     "))
            p.appendChild(newdoc.createTextNode("개봉일:" + item['openDt'] + "     "))
            p.appendChild(newdoc.createTextNode("누적관객수:" + item['audiAcc'] + "     "))
            body.appendChild(p)
            body.appendChild(br)
            body.appendChild(br)

    if tourList != None:
        body.appendChild(newdoc.createTextNode("==================== 데이트 정보 ===================="))
        body.appendChild(newdoc.createElement('br'))
        body.appendChild(newdoc.createElement('br'))
        for item in tourList:
            # BR 태그 (엘리먼트) 생성.
            br = newdoc.createElement('br')
            # create bold element
            p = newdoc.createElement('p')
            # create text node
            p.appendChild(newdoc.createTextNode("이름:" + item['title'] + "     "))
            p.appendChild(newdoc.createTextNode("주소:" + item['addr'] + "     "))
            p.appendChild(newdoc.createTextNode("정보:" + item['eventdate'] + "     "))
            p.appendChild(newdoc.createTextNode("주변시설:" + item['location'] + "     "))
            body.appendChild(p)
            body.appendChild(br)
            body.appendChild(br)
    #append Body
    top_element.appendChild(body)
    return newdoc.toxml()

def sendMail(host,movielist, tourlist,senderAddr,passwd,recipientAddr,title='제목없음',msgtext='내용없음'):
    import smtplib
    # MIMEMultipart의 MIME을 생성합니다.
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    try:
        #Message container를 생성합니다.
        msg = MIMEMultipart('alternative')
        #set message
        msg['Subject'] = title
        msg['From'] = senderAddr
        msg['To'] = recipientAddr
        msgPart = MIMEText(msgtext, 'plain')

        # 메세지에 생성한 MIME 문서를 첨부합니다.
        msg.attach(msgPart)
        html = MakeHtmlDoc(movielist,tourlist)
        htmlPart = MIMEText(html, 'html', _charset='UTF-8')
        msg.attach(htmlPart)

        print ("connect smtp server ... ")
        s = smtplib.SMTP(host,port)
        #s.set_debuglevel(1)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(senderAddr, passwd)    # 로긴을 합니다.
        s.sendmail(senderAddr , [recipientAddr], msg.as_string())
        s.close()
        print ("Mail sending complete!!!")
        return True
    except WindowsError as error:
        print(error)
        print("Mail sending Fail!!!")
        return False