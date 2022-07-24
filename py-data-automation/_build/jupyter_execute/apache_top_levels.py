#!/usr/bin/env python
# coding: utf-8

# # Apache顶级项目信息提取

# ## 引言
# 
# Apache官方网站并没有一个完整的关于顶级项目（top-level projects）的清单，但会通过blog中的announces来发布格式化的通知，比较容易提取。
# 
# 官方url有两种格式，分别是：
# - https://blogs.apache.org/foundation/entry/the_apache_software_foundation_announces + 数字
# - https://blogs.apache.org/foundation/entry/the-apache-software-foundation-announces + 数字
# 
# 两种格式的区别是使用“-”还是“_”，简单的做法是只要两者都遍历就好。以下是程序实现：

# In[ ]:


import requests
import json
import time
import sys
import re
import pandas as pd
import demjson
from bs4 import BeautifulSoup
from tqdm import tqdm


# In[ ]:


all_tops = []

for i in tqdm(range(1,103)): ## 范围需自己测试确定，或在下面代码中进一步改写try逻辑，接口返回不等于200则停止循环
    url = "https://blogs.apache.org/foundation/entry/the_apache_software_foundation_announces{}".format(i)

    payload={}
    headers = {
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
      'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja-JP;q=0.6,ja;q=0.5,zh-TW;q=0.4',
      'Connection': 'keep-alive',
      'If-None-Match': 'standard',
      'Sec-Fetch-Dest': 'document',
      'Sec-Fetch-Mode': 'navigate',
      'Sec-Fetch-Site': 'none',
      'Sec-Fetch-User': '?1',
      'Upgrade-Insecure-Requests': '1',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
      'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"macOS"'
    }
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        soup = BeautifulSoup(response.content.decode('utf-8'),'lxml')
        anno_title = soup.title.text
        anno_date = soup.select('div[class="dayTitle"]')[0].text.strip()
        anno_body = soup.select('div[class="entryBox"]')[0].text.strip()
        # 提取项目相关url
        reg = 'https://[a-z]+\.apache.org'
        pattern = re.compile(reg)
        anno_links = pattern.findall(anno_body)
        # 提取项目名称
        reg = 'Apache® (.*?)™'
        pattern = re.compile(reg)
        if pattern.search(anno_title) != None:
            project_name = re.sub(reg, r"\1", pattern.search(anno_title).group())
            # 提取项目主要描述
            reg = '{} is (.*?\.)'.format(project_name)
            pattern = re.compile(reg)
            project_desc = re.sub(reg, r"\1", pattern.search(anno_body).group())
        else:
            project_name = ''
            project_desc = ''
        anno = {'url':url, 'project_name':project_name, 'project_desc':project_desc, 'anno_title':anno_title, 'anno_date':anno_date, 'anno_links':anno_links, 'anno_body':anno_body}
    except Exception as e:
        print(url)
        continue
    all_tops.append(anno)


# In[ ]:


for i in tqdm(range(1,85)): ## 范围需自己测试确定，或在下面代码中进一步改写try逻辑，接口返回不等于200则停止循环
    url = "https://blogs.apache.org/foundation/entry/the-apache-software-foundation-announces{}".format(i)

    payload={}
    headers = {
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
      'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja-JP;q=0.6,ja;q=0.5,zh-TW;q=0.4',
      'Connection': 'keep-alive',
      'If-None-Match': 'standard',
      'Sec-Fetch-Dest': 'document',
      'Sec-Fetch-Mode': 'navigate',
      'Sec-Fetch-Site': 'none',
      'Sec-Fetch-User': '?1',
      'Upgrade-Insecure-Requests': '1',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
      'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"macOS"'
    }
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        soup = BeautifulSoup(response.content.decode('utf-8'),'lxml')
        anno_title = soup.title.text
        anno_date = soup.select('div[class="dayTitle"]')[0].text.strip()
        anno_body = soup.select('div[class="entryBox"]')[0].text.strip()
        # 提取项目相关url
        reg = 'https://[a-z]+\.apache.org'
        pattern = re.compile(reg)
        anno_links = pattern.findall(anno_body)
        # 提取项目名称
        reg = 'Apache® (.*?)™'
        pattern = re.compile(reg)
        if pattern.search(anno_title) != None:
            project_name = re.sub(reg, r"\1", pattern.search(anno_title).group())
            # 提取项目主要描述
            reg = '{} is (.*?\.)'.format(project_name)
            pattern = re.compile(reg)
            project_desc = re.sub(reg, r"\1", pattern.search(anno_body).group())
        else:
            project_name = ''
            project_desc = ''
        anno = {'url':url, 'project_name':project_name, 'project_desc':project_desc, 'anno_title':anno_title, 'anno_date':anno_date, 'anno_links':anno_links, 'anno_body':anno_body}
    except Exception as e:
        print(url)
        continue
    all_tops.append(anno)


# In[ ]:


## 最后写入到csv文件中再继续下一步使用
pd.DataFrame(all_tops).to_csv('~/data/apache_tops.csv',encoding='utf-8-sig')

