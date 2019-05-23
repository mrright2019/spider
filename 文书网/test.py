#coding:utf8
from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import random
mail_info = {
    "from": "531382443@qq.com",
    "to": "531382443@qq.com",
    "hostname": "smtp.qq.com",
    "username": "531382443@qq.com",
    "password": "xpiffsoiszbabjai",
    "mail_subject": "爬虫提醒",
    "mail_text": "",
    "mail_encoding": "utf-8"
}

def sendmail():
    smtp = SMTP_SSL(mail_info["hostname"])
    smtp.set_debuglevel(1)
    smtp.ehlo(mail_info["hostname"])
    smtp.login(mail_info["username"], mail_info["password"])
    msg = MIMEText(mail_info["mail_text"]+str(random.random()), "plain", mail_info["mail_encoding"])
    msg["Subject"] = Header(mail_info["mail_subject"], mail_info["mail_encoding"])
    msg["from"] = mail_info["from"]
    msg["to"] = mail_info["to"]
    smtp.sendmail(mail_info["from"], mail_info["to"], msg.as_string())

    smtp.quit()



sendmail();
