#coding:utf-8
import sys
import urllib2
import re
from bs4 import BeautifulSoup
from distutils.filelist import findall

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
    page = urllib2.urlopen(url)
    contents = page.read()
    soup = BeautifulSoup(contents,"html.parser")
    return(soup)


def pagination_info(area_url,start_p,end_p):
    land_agent_url_f=open("./land_agent_url_txt","w")
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
        for tag in GetHtml(url).find_all('a', class_='name project-card-item'):
            land_agent.append((tag.get_text()+"*").strip("\n"))
            land_agent_url.append((tag.get('href')+"*").strip("\n"))

        #address=[]
        for tag in soup.find_all('span', class_='position-des'):
            address.append((tag.get_text()+"*").strip("\n"))

        #price=[]
        for tag in soup.find_all('div', class_='total-price'):
            price.append((tag.get_text().strip("\n").replace(",","")+"*"))

        #update_date=[]
        for tag in soup.find_all('div', class_='building-news'):
            if tag.find_all('span',class_='title'):
                update_date.append(tag.find('span',class_='title').get_text().strip("\n"))
            else:
                update_date.append("No")
    #return(land_agent,land_agent_url,address,price,update_date)
    for link in land_agent_url:
        print >>land_agent_url_f,"%s"%(land_agent_url)
    land_agent_url_f.close()
    return(map(lambda(a,b,c,d,e):a+b+c+d+e,zip(land_agent,land_agent_url,address,price,update_date)))
    
area_url="http://gz.julive.com/project/s/zengcheng"
start_p=2
end_p=12
combine_list=pagination_info(area_url,start_p,end_p)
#combine_list=map(lambda(a,b,c,d,e):a+b+c+d+e,zip(land_agent,land_agent_url,address,price,update_date))
combine_list_to_str="\n".join(combine_list)
print(combine_list_to_str)
