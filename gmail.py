#from http.client import HTTPConnection

##global
#conn = None
#server = "api.visitkorea.or.kr"

#conn = HTTPConnection(server)
#conn.request("GET", "/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.xml?repNationCd=&targetDt=20160518&key=b2469288dbc7cf61d1484f741294e1a5&weekGb=&multiMovieYn=&")

# smtp 정보
host = "smtp.gmail.com" # Gmail SMTP 서버 주소.
port = "587"

def MakeHtmlDoc(BookList):
    from xml.dom.minidom import getDOMImplementation
    #get Dom Implementation
    impl = getDOMImplementation()

    newdoc = impl.createDocument(None, "html", None)  #DOM 객체 생성
    top_element = newdoc.documentElement
    header = newdoc.createElement('header')
    top_element.appendChild(header)

    # Body 엘리먼트 생성.
    body = newdoc.createElement('body')

    for bookitem in BookList:
        #create bold element
        b = newdoc.createElement('b')
        #create text node
        ibsnText = newdoc.createTextNode("ISBN:" + bookitem[0])
        b.appendChild(ibsnText)

        body.appendChild(b)

        # BR 태그 (엘리먼트) 생성.
        br = newdoc.createElement('br')

        body.appendChild(br)

        #create title Element
        p = newdoc.createElement('p')
        #create text node
        titleText= newdoc.createTextNode("Title:" + bookitem[1])
        p.appendChild(titleText)

        body.appendChild(p)
        body.appendChild(br)  #line end

    #append Body
    top_element.appendChild(body)

    return newdoc.toxml()

def sendMail(html,senderAddr,passwd,recipientAddr,title='제목없음',msgtext='내용없음'):
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
        bookPart = MIMEText(html, 'html', _charset = 'UTF-8')

        # 메세지에 생성한 MIME 문서를 첨부합니다.
        msg.attach(msgPart)
        msg.attach(bookPart)
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
    except:
        print("Mail sending Fail!!!")
        return False