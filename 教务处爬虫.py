from email import header
import requests
from lxml import etree
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import json
import pymysql
import time
#数据库部分参考https://python3webspider.cuiqingcai.com/5.2-guan-xi-xing-shu-ju-ku-cun-chu#7-cha-xun-shu-ju

def sendemail(title,id):
    mail_host='smtp.111.com'
    mail_user='K.Going666'  #发件用户名
    mail_pass='47eFf8NWzAnbgXaB'  #授权码
    newsurl='http://jw.scut.edu.cn/zhinan/cms/article/view.do?type=posts&id='+id
    newstitle=title

    sender='K.Going666@111.com'#发送者邮箱
    receivers='1754423248@qq.com'#接受者邮箱
    message=MIMEText('教务处更新了，请立即查看:'+ newstitle+','+newsurl,'plain','utf-8')
    message['From']=Header('K.Going666@111.com','utf-8')
    message['To']=Header('1754423248@qq.com','utf-8')

    title='教务处通知更新'
    message['Subject']=Header(title,'utf-8')


    #smtpObj=smtplib.SMTP_SSL()
    #smtpObj.connect(mail_host,465) 
    smtpObj=smtplib.SMTP_SSL(mail_host,465)
    smtpObj.login(mail_user,mail_pass)
    smtpObj.sendmail(sender,receivers,message.as_string())
    smtpObj.quit()
    print ("邮件发送成功")


#数据库连接
db=pymysql.connect(host='localhost',user='pytestuser',password='123456',database='pytest')
cursor=db.cursor()

#定义post消息头
url = 'http://jw.scut.edu.cn/zhinan/cms/article/v2/findInformNotice.do'
User_Agent='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36 SE 2.X MetaSr 1.0'
data={'category': '0','tag':'0','pageNum':'1','pageSize': '15','keyword':''}
headers={'Accept': '*/*',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '47',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'DNT':'1',
        'Host':'jw.scut.edu.cn',
        'Origin': 'http://jw.scut.edu.cn',
        'Referer': 'http://jw.scut.edu.cn/zhinan/cms/toPosts.do?category=0',
        'User-Agent':User_Agent}

#爬取
r=requests.post(url,data=data,headers=headers)
a=json.loads(r.text) #r.text中的内容为json形式，直接使用json.laods解析

#初始插入数据
'''for i in range(0,11):
        newsid=a['list'][i]['id']
        title=a['list'][i]['title']
        createtime=a['list'][i]['createTime']
        print(newsid+'\t'+title+'\t'+createtime)
        #插入数据
        data={
        'ID':newsid,
        'title':title,
        "createtime":createtime
        }

        table ='newssheet'
        keys=','.join(data.keys())
        values=','.join(['%s']*len(data))
        sql='INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table,keys=keys,values=values)

        if cursor.execute(sql,tuple(data.values())):
                print('success')
                db.commit()
        else:
                print('failed')
                db.rollback()
        
db.close()
'''

#查询数据
'''condition="ID = 'ff80808179e44d41017ac6c7169d0061'"
table='newssheet'
sql= "SELECT * FROM {table} WHERE {condition}".format(table=table,condition=condition)
cursor.execute(sql)

print('Count:', cursor.rowcount)
row=cursor.fetchone()
if row:
        print('存在row:',row)
        row=cursor.fetchone()
else:
        print(row)'''

for i in range(0,5):
        newid=a['list'][i]['id']
        condition="ID = '{newid}'".format(newid=newid)
        sql="SELECT * FROM newssheet HAVING {condition}".format(condition=condition)
        cursor.execute(sql)
        row=cursor.fetchone()
        if a['list'][i]['isNew']==True and row==None:
                sql='INSERT INTO newssheet(ID,title,createtime) VALUES (%s,%s,%s)'
                cursor.execute(sql,(a['list'][i]['id'],a['list'][i]['title'],a['list'][i]['createTime']))
                
                sendemail(a['list'][i]['title'],a['list'][i]['id'])
                time.sleep(5)
