import requests
from lxml import etree
import re
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def sendemail(lianjie):
    mail_host='' #smtp服务器地址
    mail_user=''  #发件用户名
    mail_pass=''  #授权码
    newsurl=lianjie

    sender=''#发送者邮箱
    receivers=''#接受者邮箱
    message=MIMEText('通知更新了，请立即查看'+ newsurl,'plain','utf-8') #邮件正文内容
    message['From']=Header('','utf-8') #设置发送者
    message['To']=Header('','utf-8') #设置接受者

    title='Python测试' #邮件标题
    message['Subject']=Header(title,'utf-8')


    #smtpObj=smtplib.SMTP_SSL()
    #smtpObj.connect(mail_host,465) 
    smtpObj=smtplib.SMTP_SSL(mail_host,465)
    smtpObj.login(mail_user,mail_pass)
    smtpObj.sendmail(sender,receivers,message.as_string())
    smtpObj.quit()
    print ("邮件发送成功")

url = 'http://www2.scut.edu.cn/cs/22291/list.htm'
r=requests.get(url)
r.encoding='utf-8'
html = etree.HTML(r.text)

title = html.xpath('//*[@id="wp_news_w27"]/ul/li[1]/a/@title')
time= html.xpath('//*[@id="wp_news_w27"]/ul/li[1]/span/text()')
lianjielist= html.xpath('//*[@id="wp_news_w27"]/ul/li[1]/a/@href')
lianjie='www2.scut.edu.cn' + lianjielist[0]


if time[0] !='2021-07-19' and re.search('xxx',title[0]):  #xxx为想要关注的通知名，比如：分流
    sendemail(lianjie)


