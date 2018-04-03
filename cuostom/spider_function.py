#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
from browser_client import GetHtml

def pagination_info(area_url,start_p,end_p):
    all_land_agent_links=[area_url]
    for i in range(start_p,end_p):
        all_land_agent_links.append(all_land_agent_links[0]+"-z"+str(i))
    land_agent=[]
    land_agent_url=[]
    address=[]
    price=[]
    update_date=[]
    for url in all_land_agent_links:
        soup=GetHtml(url)
        for tag in soup.find_all('a', class_='name project-card-item'):
            land_agent.append((tag.get_text()+"*").strip("\n"))
            land_agent_url.append((tag.get('href')).strip("\n"))

        #address=[]
        for tag in soup.find_all('span', class_='position-des'):
            address.append(("*"+tag.get_text()+"*").strip("\n"))

        #price=[]
        for tag in soup.find_all('div', class_='total-price'):
            price.append((tag.get_text().strip("\n").replace(",","")+"*"))

        #update_date=[]
        for tag in soup.find_all('div', class_='building-news'):
            if tag.find_all('span',class_='title'):
                update_date.append(tag.find('span',class_='title').get_text().strip("\n"))
            else:
                update_date.append("No")

    land_agent_url_f=open("./land_agent_url_txt","w")
    for link in land_agent_url:
        print >>land_agent_url_f,"%s"%(link)
    land_agent_url_f.close()
    return(map(lambda(a,b,c,d,e):a+b+c+d+e,zip(land_agent,land_agent_url,address,price,update_date)))


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
            return(tag.get_text().replace("报价更新时间：","")
            break
        #else:
        #    return("No_Price_Update_Time")

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

def all_house_type_link(soup):
    house_type_url_txt_f=open('./house_type_url_txt','a')
    for tag in soup.find_all('a',class_='look-more'):
        print >>house_type_url_txt_f,"%s"%(tag.get('href'))
    house_type_url_txt_f.close()

def house_type_info(soup):
    for tag in soup.find_all('span',class_='type'):
        global house_type
        house_type=tag.get_text()
    
    for tag in soup.find_all('img',class_='thumb'):
        global house_type_pic_link
        house_type_pic_link=tag.get('src')

    return("%s*%s"%(house_type,house_type_pic_link))

def house_properties(soup):
    house_property_keys = []
    for tag in soup.find_all('span',class_='key'):
        house_property_keys.append(tag.get_text())
    
    house_property_values = []
    for tag in soup.find_all('span',class_='value'):
        house_property_values.append(tag.get_text())
    
    house_properties=map(lambda(a,b):a+b,zip(house_property_keys,house_property_values))
    str_house_properties = '*'.join(house_properties)
    return(str_house_properties)
