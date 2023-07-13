

import imaplib


def get_mail_client(email_address):
    SMTP_SERVER = "imap.gmail.com"
    SMTP_PORT = 993
    
    password = ""

    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
    mail.login(email_address, password)
    mail.select('SamasungTest')
    return mail


print(get_mail_client('ltsenovoy@gmail.com'))