# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header
import urllib2
import re
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def print_obj(obj): 
    print '\n'.join(['%s:%s' % item for item in obj.__dict__.items()])

def send_email(price): 
    mail_host="host" 
    mail_user="user"
    mail_pass="pass" 

    sender = 'sender'
    receivers = 'receivers'

    message = MIMEText(price, 'plain', 'utf-8')
    message['From'] = Header('from')
    message['To'] = Header('to')

    subject = 'PES2018'
    message['Subject'] = Header(subject,'utf-8')

    try:
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(mail_host,25)
        smtpObj.login(mail_user,mail_pass)  
        smtpObj.sendmail(sender,receivers,message.as_string())
    except smtplib.SMTPException:
        print u"Error: Can not send email"

def get_price(url):
    price = 'null'
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0")
    browser = webdriver.PhantomJS(executable_path='D:\Python27\Scripts\phantomjs.exe',desired_capabilities=dcap)
    try:
        browser.get(url)
        time.sleep(20)
        contents = browser.find_elements_by_class_name('price')
        for content in contents:
            if content.text:
                price = content.text
                break
        browser.quit()
    except:
        price = 'null'
    return price

def main():
    line = 'HK$400.00'
    url = 'https://store.playstation.com/#!/zh-hans-hk/%e6%b8%b8%e6%88%8f/pes-2018(winning-eleven-2018)/cid=HP0101-CUSA08289_00-PES2018000000000'

    while True:
        price = get_price(url)
        if not cmp (price,'null'):
            continue
        if cmp (line,price) > 0:
            send_email(price)
            print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'---->'+price
            line = price

if __name__ == "__main__":
    main()
    
