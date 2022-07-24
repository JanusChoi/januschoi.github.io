#!/usr/bin/env python
# coding: utf-8

# # 万方下载论文重命名
# 
# 万方直接下载的论文原文pdf文件名会变成一串编码，目测可解码，迅速批量操作如下

# In[ ]:


import os
import urllib

filepath="/Users/januswing/Downloads" # 存放pdf的路径
all_files = os.listdir(filepath)
for file in all_files:
    if '%' in file and file[-3:] == 'pdf': # 这里条件是文件名中包含 % 且后缀为pdf，可根据需要修改
        filename = file[:-4]
        filename = urllib.parse.unquote(filename)
        filename = filename.replace('/','') # 有些文件名包含 / 会导致报错，因此需要替换掉
        os.rename('{}/{}'.format(filepath, file), '{}/{}.pdf'.format(filepath,filename)) # 修改为解码后文件名即可

