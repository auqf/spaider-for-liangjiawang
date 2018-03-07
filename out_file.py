#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
from browser_client import GetHtml
from spider_function import pagination_info,start_time,price_update_time,detail_info,around_info,around_info

area_url="http://gz.julive.com/project/s/zengcheng"
#default url format:"http://gz.julive.com/project/20003323.html",即地产商首页链接地址
start_p=2
end_p=12
combine_list=pagination_info(area_url,start_p,end_p)
combine_list_to_str="\n".join(combine_list)

land_agent_info_f=open('./land_agent_info','w')
reload(sys)
sys.setdefaultencoding('utf-8')
print >>land_agent_info_f,"%s*%s*%s*%s*%s" %('地产商','地产商主页','楼盘地址','均价','最新更新时间')
print >>land_agent_info_f, "%s" %(combine_list_to_str)
land_agent_info_f.close()


land_agent_detail_info_f=open('./land_agent_detail_info','w')
print >>land_agent_detail_info_f,"%s*%s*%s*%s*%s*%s*%s" %('地产商主页','首次动态时间','报价更新时间','最新开盘','最早交房','产权年限','周边环境')
with open('./land_agent_url_txt') as fd:
    while True:
        url=fd.readline()
        if not url:
            break
        #soup=GetHtml(url)
        a=start_time(GetHtml(url.replace(".html","/news.html")))#首次动态时间
        b=price_update_time(GetHtml(url.replace(".html","/ht.html")))#报价更新时间
        c=detail_info(GetHtml(url.replace(".html","/details.html")))#最新开盘,最早交房,产权年限
        d=around_info(GetHtml(url.replace(".html","/su.html")))
        e=around_info(GetHtml(url.replace(".html","/su.html")))
        print >>land_agent_detail_info_f,"%s*%s*%s%s*%s*%s"%(url.strip("\n"),a,b,c,d,e)
f.close()
