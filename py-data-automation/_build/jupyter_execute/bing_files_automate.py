#!/usr/bin/env python
# coding: utf-8

# # 批量下载文件并存入Zotero（cn.bing.com）
# 
# ## 优化项
# 
# - [ ] PDF解释+Zotero写入可多线程并发进行
# - [ ] 优化摘要提取
# - [ ] 增加PDF提取信息：作者，日期
# - [ ] 可指定Zotero Collection
# - [ ] 自动新建文件夹

# In[1]:


import requests
import json
import time
import datetime
import sys
import re
import pandas as pd
import demjson
from bs4 import BeautifulSoup
from tqdm import tqdm
import pymongo
from threading import Thread
import queue
import PyPDF2
from pyzotero import zotero


# In[2]:


# 参数设置

## 起始页设置
start_page = 1
end_page = 1
## 本次检索主题
theme = 'smart_retail'
## 文件存储位置
file_path = '/Users/januswing/Downloads/{}'.format(theme)
## 文件类型
file_type = 'pdf'
## 检索词或检索式
keyword = '智慧零售'
## Zotero接口参数
library_id = '5012819'
library_type = 'user'
api_key = 'FkXpNmTlLwqDnhKxS2n2zgoj'

search_string = 'filetype:{}+{}'.format(file_type, keyword)
pages = range(start_page - 1, end_page)
batch_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")


# In[3]:


# 本地 MongoDB 设置
MongoServer = 'mongodb://localhost:27017/'
MongoDB = 'runoobdb'
Collection = '{}_{}'.format(theme, batch_id)

myclient = pymongo.MongoClient(MongoServer)
mydb = myclient[MongoDB]

mycol = mydb[Collection]


# In[4]:


# 简易多线程并发器
class FactorizeThread(Thread):
    """
    多线程并发采集
    """
    def __init__(self, param, queue):
        super().__init__()
        self.param = param
        self.queue = queue

    def run(self):
        try:
            self.res = crawler(self.param)
        finally:
            self.queue.get()
            self.queue.task_done()


# In[5]:


# 数据采集核心函数
def crawler(param):
    in_first = 10 * param['page'] + 1
    url = "https://cn.bing.com/search?q={0}&qs=n&sp=-1&pq={0}&sc=8-17&sk=&cvid=F3FE0F2FF663402D9E91FADB93A9A4BB&first={1}&FORM=PERE".format(search_string, in_first)
    payload={}
    headers = {
      'authority': 'cn.bing.com',
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
      'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja-JP;q=0.6,ja;q=0.5,zh-TW;q=0.4',
      'cookie': 'MUID=0D5070894F656FEF3F1360644E476E11; MUIDB=0D5070894F656FEF3F1360644E476E11; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=A420B1CE3A0C4BAB9B0A75C34E48D47E&dmnchg=1; MUIDV=NU=1; _FP=hta=off; _UR=QS=0&TQS=0; _clck=tx1nki|1|f1q|0; USRLOC=HS=1&DLOC=LAT=23.128081|LON=113.3345447|A=61.477|N=%e5%a4%a9%e6%b2%b3%e5%8c%ba%2c+%e5%b9%bf%e5%b7%9e%e5%b8%82|C=|S=|TS=220526093840|ETS=220526094840|; imgv=flts=20220531; _TTSS_IN=hist=WyJhZiIsInpoLUhhbnMiLCJlbiIsImF1dG8tZGV0ZWN0Il0=; _TTSS_OUT=hist=WyJhZiIsImVuIiwiemgtSGFucyJd; _tarLang=default=zh-Hans; ZHCHATSTRONGATTRACT=TRUE; SUID=M; _EDGE_S=SID=158903A432E162981EE4126033AB6373; _SS=SID=158903A432E162981EE4126033AB6373; ABDEF=V=13&ABDV=11&MRNB=1655351524960&MRB=0; SRCHUSR=DOB=20211112&T=1655358959000&TPC=1655337133000; ipv6=hit=1655362560080&t=4; _HPVN=CS=eyJQbiI6eyJDbiI6MTg3LCJTdCI6MiwiUXMiOjAsIlByb2QiOiJQIn0sIlNjIjp7IkNuIjoxODcsIlN0IjowLCJRcyI6MCwiUHJvZCI6IkgifSwiUXoiOnsiQ24iOjE4NywiU3QiOjEsIlFzIjowLCJQcm9kIjoiVCJ9LCJBcCI6dHJ1ZSwiTXV0ZSI6dHJ1ZSwiTGFkIjoiMjAyMi0wNi0xNlQwMDowMDowMFoiLCJJb3RkIjowLCJHd2IiOjAsIkRmdCI6bnVsbCwiTXZzIjowLCJGbHQiOjAsIkltcCI6MTAwN30=; ZHCHATWEAKATTRACT=TRUE; SRCHHPGUSR=SRCHLANG=en&BRW=S&BRH=T&CW=1137&CH=1014&SW=1800&SH=1169&DPR=2&UTC=480&DM=1&WTS=63790955764&HV=1655360790&BZA=0&PV=12.4.0; SNRHOP=I=&TS=; SNRHOP=I=&TS=; MUIDB=0D5070894F656FEF3F1360644E476E11',
      'referer': '',
      'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
      'sec-ch-ua-arch': '"arm"',
      'sec-ch-ua-bitness': '"64"',
      'sec-ch-ua-full-version': '"102.0.5005.115"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-model': '""',
      'sec-ch-ua-platform': '"macOS"',
      'sec-ch-ua-platform-version': '"12.4.0"',
      'sec-fetch-dest': 'document',
      'sec-fetch-mode': 'navigate',
      'sec-fetch-site': 'same-origin',
      'sec-fetch-user': '?1',
      'upgrade-insecure-requests': '1',
      'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data=payload, timeout=60)
    soup = BeautifulSoup(response.content.decode('utf-8'),'lxml')
    for doc_link in soup.select('div[class="b_title"]'):
        file_url = doc_link.a['href']
        file_title = doc_link.text.replace('[PDF]','').replace(' ','').replace('/','')
        try:
            myfile = requests.get(file_url, timeout=120)
            file_saved = '{}/{}.pdf'.format(file_path, file_title)
            open(file_saved,'wb').write(myfile.content)
        except Exception as e:
            print('{} get file: {}'.format(file_title, e.__str__()))
            continue
        finally:
            file_data = {'file_url':file_url, 'file_title':file_title, 'file_saved':file_saved}
            mycol.insert_one(file_data)


# In[6]:


# pdf解释函数
def pdf_explain(file_data):
    name = file_data['file_title']
    file = file_data['file_saved']
    pdf_meta = {}
    pdf_meta['status']='success'
    try:
        pdf_file = PyPDF2.PdfFileReader(open(file, 'rb'))
        docinfo = pdf_file.getDocumentInfo()
    except Exception as e:
        print('{} file explain error: {}'.format(name, e.__str__()))
        pdf_meta = {'status':'failed', 'name':name, 'file':file}
        return pdf_meta
    
    for key in docinfo:
        key_new = key.replace('/','')
        value_new = docinfo[key].replace('/','').replace('D:','').replace("+08'00'",'')
        pdf_meta[key_new] = value_new

    words = '引言|摘要'
    astract = ''
    for page in pdf_file.pages:
        word_list = words.split('|')
        for word in word_list:
            try:
                pageinfo = page.extract_text()
            except Exception as e:
                pageinfo = ''
                continue
            if word in pageinfo:
                astract = astract + page.extract_text()
    pdf_meta['astract'] = astract
    pdf_meta['name'] = name
    return pdf_meta


# In[7]:


# 数据采集运行
para = []
threads = []
maxThreads = 10 # 并发数
q = queue.Queue(maxThreads)
pages = range(start_page - 1, end_page)
for page in pages:  # loop cityname
    param = {'page': page}
    q.put(param)
    thread = FactorizeThread(param, q)
    thread.start()
    threads.append(thread)
q.join()


# In[8]:


# pdf解释运行
for line in mycol.find():
    pdf_meta = pdf_explain(line)
    if pdf_meta['status'] == 'failed':
        print('{}文件解析失败: {}'.format(pdf_meta['name'], pdf_meta['file']))
    else:
        zot = zotero.Zotero(library_id, library_type, api_key)
        template = zot.item_template('webpage')
        template['title'] = pdf_meta['name']
        template['abstractNote'] = pdf_meta['astract']
        res = zot.create_items([template])
        item_id = res['successful']['0']['key']
        attachment_path = line['file_saved']
        zot.attachment_simple([attachment_path], item_id)


# In[ ]:




