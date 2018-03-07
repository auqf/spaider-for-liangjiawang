#!/usr/bin/python
# -*- coding: UTF-8 -*-
import urllib2
import sys
import urllib2
import re
from bs4 import BeautifulSoup
#from distutils.filelist import findall

def GetHtml(url):
    #req_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    #'Accept':'text/html;q=0.9,*/*;q=0.8',
    #'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    #'Accept-Encoding':'utf-8',
    #'Connection':'close',
    #'Referer':None #注意如果依然不能抓取的话，这里可以设置抓取网站的host
    #}
    #req_timeout = 5
    #req = urllib2.Request(url,None,req_header)
    #resp = urllib2.urlopen(req,None,req_timeout)
    #html = resp.read()
    #soup = BeautifulSoup(html,"html.parser")
    #return soup
    page = urllib2.urlopen(url)
    contents = page.read()
    soup = BeautifulSoup(contents,"html.parser")
    return(soup)


def start_time(soup):
    news_date=[]
    for tag in soup.find_all('div',class_='date'):
        news_date.append(tag.get_text())
    if len(news_date) > 0:
        return(news_date[-1])
    else:
        return("No_Start_Time")

def price_update_time(soup):
    for tag in soup.find_all('div',class_='td'):
        if re.match(u"报价更新时间",tag.get_text()):
            return(tag.get_text())
            break
        else:
            return("No_Price_Update_Time")

def detail_info(soup):
    a=[]#the latest opening
    b=[]#the earliest delivery
    c=[]#years of property rights
    for tag in soup.find_all('li'):
        if tag.find('div',class_='th') and tag.find('div',class_='txt'):
            if re.search(u"最新",tag.get_text()):
                a.append(tag.get_text().replace("\n",""))
            if re.search(u"最早",tag.get_text()):
                b.append(tag.get_text().replace("\n",""))
            if re.search(u"产权",tag.get_text()):
                c.append(tag.get_text().replace("\n",""))
    if len(a)>0 and len(b)>0 and len(c)>0:
        return("%s%s%s" %(str(a[0]).replace("最新开盘","*"),str(b[0]).replace("最早交房","*"),str(c[0]).replace("产权年限","*")))
    else:
        return("No_Detail_Info1*No_Detail_Info2*No_Detail_Info3")

def around_info(soup):
    around_value = []
    for tag in soup.find_all('ul',class_="zb-list lk-list"):
        if tag.find("p"):
            around_value.append(tag.find("p").get_text())
        else:
            around_value.append(("No"))
    around_key=["公交:","地铁:","学校:","购物:","医疗:"]
    around_env=map(lambda(x,y):x+y,zip(around_key,around_value))
    str_around_env = "*".join(around_env)
    if str_around_env:
        return(str_around_env)
    else:
        return("error")

f=open('./land_agent_link_detail','w')
print >>f,"%s*%s*%s*%s*%s*%s*%s" %('地产商主页','首次动态时间','报价更新时间','最新开盘','最早交房','产权年限','周边环境')
with open('./land_agent_url_txt') as fd:
    while True:
        reload(sys)
        sys.setdefaultencoding('utf-8')
        #default url format:"http://gz.julive.com/project/20003323.html",即地产商首页链接地址
        url=fd.readline()
        if not url:
            break
        #soup=GetHtml(url)
        a=start_time(GetHtml(url.replace(".html","/news.html")))#首次动态时间
        b=price_update_time(GetHtml(url.replace(".html","/ht.html")))#报价更新时间
        c=detail_info(GetHtml(url.replace(".html","/details.html")))#最新开盘,最早交房,产权年限
        d=around_info(GetHtml(url.replace(".html","/su.html")))
        e=around_info(GetHtml(url.replace(".html","/su.html")))
        print >>f,"%s*%s*%s%s*%s*%s"%(url.strip("\n"),a,b,c,d,e)
f.close()
