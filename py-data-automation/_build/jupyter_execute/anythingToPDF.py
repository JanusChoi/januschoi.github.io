#!/usr/bin/env python
# coding: utf-8

# # 链接生成PDF并保存Zotero

# 
# 将免登录的页面链接，生成pdf文件，并写入到Zotero
# 使用场景举例：
# - 需要收藏一篇微信公众号到Zotero
# - 在程序中输入链接，如：https://mp.weixin.qq.com/s/IFdFunIx9YoVeXIXz_GpUg
# - 运行程序
# - 程序将公众号内容自动导出pdf，并存储到Zotero，类型=document
# 
# 前置条件：
# - wkhtmltopdf: 安装参考 https://github.com/JazzCore/python-pdfkit/wiki/Installing-wkhtmltopdf
# - pdfkit: pip install pdfkit
# 
# 已知缺陷：
# - pdfkit导出时一些图片无法保存到pdf

# In[1]:


import pdfkit
import requests
import re,time
import pandas as pd
from bs4 import BeautifulSoup
from pyzotero import zotero


# In[2]:


## 要保存的网页链接
webpage_url = 'https://mp.weixin.qq.com/s/Y5bEBezJupY1GQrrWxPaXw'
## 存储路径
filepath = '/Users/januswing/data'
## Zotero接口参数
library_id = ''
library_type = ''
api_key = ''
## Zotero Collection 名称（可不指定）
target_collection_name = '项目文档'


# In[3]:


headers = {
  'authority': 'mp.weixin.qq.com',
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja-JP;q=0.6,ja;q=0.5,zh-TW;q=0.4',
  'cache-control': 'max-age=0',
  'if-modified-since': 'Tue, 12 Jul 2022 14:33:55 +0800',
  'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"macOS"',
  'sec-fetch-dest': 'document',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'none',
  'sec-fetch-user': '?1',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}

response = requests.request("GET", webpage_url, headers=headers)
whole_text = response.text
soup = BeautifulSoup(response.content.decode('utf-8'),'lxml')


# In[4]:


## 提取文章标题 & 公众号名称
document_title = soup.select('h1')[0].text.replace('\n','').replace(' ','')
for span in soup.select('div[id="meta_content"]')[0].select('span'):
    if span.a:
        document_author = span.a.text.replace('\n','').replace(' ','')
## 提取文章发布时间
pattern = re.compile('"[0-9]+",0,document.getElementById\("publish_time"\)')
publish_timestamp = pattern.search(whole_text).group().replace('",0,document.getElementById("publish_time")','').replace('"','')
## 转换成localtime
time_local = time.localtime(int(publish_timestamp))
## 转换成新的时间格式
document_publish_time = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
file_timemark = time.strftime("%Y%m%d",time_local)
## 生成并保存为pdf
document_save_path = '{}/{}_{}.pdf'.format(filepath, document_title.replace('.',''), file_timemark)
pdfkit.from_url(webpage_url, document_save_path)


# In[5]:


# 连接 Zotero
zot = zotero.Zotero(library_id, library_type, api_key)
# 提取 collections 信息
collections = []
for collection in zot.collections():
    collections.append(collection)

df_col = pd.DataFrame()
for col in collections:
    df_col = df_col.append(col['data'], ignore_index=True)

if target_collection_name != '':
    target_collection_id = df_col[df_col['name']==target_collection_name]['key'].iloc[0]


# In[6]:


# 保存Zotero条目
## 请保证云存储空间充足
template = zot.item_template('document')
template['title'] = document_title
template['creators'] = [{'creatorType': 'author', 'name': document_author}]
template['date'] = document_publish_time
template['url'] = webpage_url
if target_collection_name != '':
    template['collections'] = [target_collection_id]
res = zot.create_items([template])
item_id = res['successful']['0']['key']
attachment_path = document_save_path
zot.attachment_simple([attachment_path], item_id)


# In[ ]:




