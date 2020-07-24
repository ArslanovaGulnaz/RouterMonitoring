import imaplib
import email
import re
from email.header import decode_header, make_header


def main():
    pointStatus = ""
    pointName = ""
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    
    mail.login('login', 'pass')
    mail.list()

    dataArr = []

    # Выводит список папок в почтовом ящике.
    mail.select("inbox")  # Подключаемся к папке "входящие".
    result, data = mail.search(None, "FROM '<backup mail> OR <zabbix mail>") #"FROM 'msteambckup@gmail.com'
    ids = data[0]  # строка номеров писем
    '''--- Для всех писем---'''
    for id in ids.split():
        result, data = mail.fetch(id, 'RFC822')  # will read the first email
        email_content = data[0][1]
        msg = email.message_from_bytes(email_content)  # this needs to be corrected in your case
        emailDate = msg["Date"]
        emailSubject = msg["Subject"]
        decodedSubject = decode_header(emailSubject)
        decodedSubject = str(make_header(decodedSubject))
        subjectWords = re.sub(r'[.!,;? ]', " ", decodedSubject).split()
        '''---Проверка на название точки в теме письма---'''
        for subjWord in subjectWords:
            if "cAP_Scene" in subjWord or 'wAP_Sklad' in subjWord or 'wAP_Stolovaya' in subjWord\
                    or 'cAP_ITShtab' in subjWord or '02_Shtab' in subjWord or '05_Scene' in subjWord\
                    or '04_Shater' in subjWord or 'wAP_Info' in subjWord or '07_Sphere' in subjWord\
                    or 'wAP_3Shater' in subjWord or '01_Koryltay' in subjWord or '03_SeletLive' in subjWord\
                    or 'Forum_main_mikrotik_WAN1' in subjWord or 'Forum_main_mikrotik_WAN2' in subjWord:
                pointName = subjWord
        '''---Проверка статуса точки---'''
        if 'Down' in decodedSubject:
            pointStatus = 'Down'
        if 'Up' in decodedSubject or 'UP' in decodedSubject:
            pointStatus = 'Up'
        '''---Строка с датой, именем точки, ее статусом---'''
        dataStr = emailDate + ' ' + pointName + ' ' + pointStatus
        dataArr.append(dataStr)
    return (dataArr)
print(main())
