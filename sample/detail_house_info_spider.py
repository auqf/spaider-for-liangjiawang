#!/usr/bin/python
#coding:utf-8
import sys
from browser_client import GetHtml

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

house_type_detail_info_f=open('./house_type_detail_info','w')
with open('./house_type_url_txt') as fd:
    while True:
        url=fd.readline()
        if not url:
            break
        #soup=GetHtml(url)
        a=house_type_info(GetHtml(url))
        b=house_properties(GetHtml(url))
        reload(sys)
        sys.setdefaultencoding('utf-8')
        print >>house_type_detail_info_f,"%s*%s*%s"%(url.strip("\n"),a,b)
house_type_detail_info_f.close()
