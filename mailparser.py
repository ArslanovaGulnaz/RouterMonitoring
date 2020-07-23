import imaplib
import email
import re
from email.header import decode_header, make_header


def main():
    pointStatus = ""
    pointName = ""
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    #mail.login('gulnaz.arslanova@msteam.org', 'MasterMoriarty907')
    mail.login('pointsmonitoring@gmail.com', 'P@ssw0rd2020')
    mail.list()

    dataArr = []

    # Выводит список папок в почтовом ящике.
    mail.select("inbox")  # Подключаемся к папке "входящие".
    #result, data = mail.search(None, "SUBJECT '[FORUM]'")
    result, data = mail.search(None, "FROM 'msteambckup@gmail.com")
    ids = data[0]  # строка номеров писем
    # print(result, ids.split())
    '''
    --- Для всех писем---'''
    for id in ids.split():
        result, data = mail.fetch(id, 'RFC822')  # will read the first email
        email_content = data[0][1]
        msg = email.message_from_bytes(email_content)  # this needs to be corrected in your case
        emailDate = msg["Date"]
        emailSubject = msg["Subject"]
        # decodedSubject = emailSubject.encode().decode('utf-8') декодирует по частям
        decodedSubject = decode_header(emailSubject)
        decodedSubject = str(make_header(decodedSubject))
        subjectWords = re.sub(r'[.!,;? ]', " ", decodedSubject).split()
        for subjWord in subjectWords:
            if "cAP_Scene" in subjWord or 'wAP_Sklad' in subjWord or 'wAP_Stolovaya' in subjWord\
                    or 'cAP_ITShtab' in subjWord or '02_Shtab' in subjWord or '05_Scene' in subjWord\
                    or '04_Shater' in subjWord or 'wAP_Info' in subjWord or '07_Sphere' in subjWord\
                    or 'wAP_3Shater' in subjWord or '01_Koryltay' in subjWord or '03_SeletLive' in subjWord:
                pointName = subjWord
        # pointName = re.findall(r"\b\w+\bWAN", decodedSubject)
        if 'Down' in decodedSubject:
            pointStatus = 'Down'
        if 'Up' in decodedSubject or 'UP' in decodedSubject:
            pointStatus = 'Up'
        # print(emailDate, '|', decodedSubject, ' | ', pointStatus, ' | ', pointName, end='\n' )
        #print(emailDate, ' | ', pointName, ' | ', pointStatus, end='\n')
        #dataArr.extend(emailDate, pointName, pointStatus)

        dataStr = emailDate + ' ' + pointName + ' ' + pointStatus
        dataArr.append(dataStr)
    #return (emailDate, pointName, pointStatus)
    return (dataArr)
print(main())


''' НЕ РАБОТАЕТ
---Для последнего письма---
latest_id = (ids.split())[-1]
data = mail.fetch(latest_id, 'RFC822')# will read the first email
email_content = data[0][1]
msg = email.message_from_string(email_content)# this needs to be corrected in your case
emailDate = msg["Date"]
emailSubject = msg["Subject"]
#decodedSubject = emailSubject.encode().decode('utf-8') #декодирует по частям
decodedSubject = decode_header(emailSubject)
decodedSubject = str(make_header(decodedSubject))
subjectWords = re.sub(r'[.!,;? ]', " ", decodedSubject).split()
for subjWord in subjectWords:
    if "WAN" in subjWord:
        pointName = subjWord
#pointName = re.findall(r"\b\w+\bWAN", decodedSubject)
if 'PROBLEM' in decodedSubject:
    pointStatus = 'PROBLEM'
if 'OK' in decodedSubject:
    pointStatus = 'OK'
print(emailDate, '|', decodedSubject, ' | ', pointStatus, ' | ', pointName, end='\n' )
print(emailDate, emailSubject)
'''
