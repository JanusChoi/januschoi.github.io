#!/usr/bin/env python
# coding: utf-8

# # Word文档资料整理工作流
# 
# 因为工作中总有大量的word文档，其中又有大部分是需要阅读学习的资料，因此初步希望能够将word转成pdf，并写入到Zotero，使用在一个界面中进行学习。
# 后续也更方便在Zotero中阅读，划线标记，并收集为Notes导出使用
# 
# - doc转pdf放入Zotero  
# - pdf标注提取  
# - Annotation转换为note  
# - note批量整理--通过search筛选器
# 
# 目前效果：
# 
# ## 在Finder中右键选中docs文件，选择Quick Action>word2pdf，文件就会自动转为pdf并写入到Zotero
# 
# ## 踩坑记录
# - 打开word时总弹出授权请求，chmod无法解决，但无论授权窗口点击确认或取消都可以执行成功，怎么可以省掉这个步骤？

# In[ ]:


from docx2pdf import convert
import os
import re


# In[ ]:


def add_escape(value):
    reserved_chars = r'''?&|!{}[]()^~*:\\"'+ '''
    replace = ['\\' + l for l in reserved_chars]
    trans = str.maketrans(dict(zip(reserved_chars, replace)))
    return value.translate(trans)


# In[ ]:


doc_file = '/Users/januswing/Nutstore Files/projects/doc_智慧港口建设指南/智慧港口-素材汇总/模板1-智能生产作业v2.0(1)-华东电子.docx'
doc_file_cmd = add_escape(doc_file)
pdf_temp_path = '/Users/januswing/data'
tmp_symbol_loc = [each.start() for each in re.finditer("/", doc_file)]
pdf_temp_name = '{}{}{}'.format(pdf_temp_path, doc_file[tmp_symbol_loc[-1]:len(doc_file)-4], 'pdf')
pdf_temp_name_cmd = add_escape(pdf_temp_name)


# In[ ]:


os.system('chmod 777 {}'.format(doc_file_cmd))
os.system('rm -f {}'.format(pdf_temp_name_cmd))

convert(doc_file, pdf_temp_name)


# ## 已实现的部分优化
# 
# 想想如果每一次你拿到一个文件，还要把文件名放到脚本里面，然后执行程序，再把生成的pdf文件丢进Zotero，整个过程仍然非常繁琐。
# 于是我想到可以通过苹果的Automator调用一个shell脚本，把上面的过程一次性完成。
# 过程如下：
# 
# ### 1. 配置Automator
# 
# 打开Automator，新建一个workflow，选择Quick Action，然后设置如下
# ![](https://tva1.sinaimg.cn/large/e6c9d24egy1h4i2e797bsj20wp0azdgr.jpg)
# 
# shell脚本示例如下（使用时记得修改为你的路径）
# 
# ```{shell}
# #!/bin/bash
# # set -e
# 
# # 获取路径及文件名
# filename=$1
# echo "输入文件为:"${filename}  >> ~/data/word2pdf.log
# 
# # 执行python
# /Users/januswing/opt/anaconda3/envs/py37/bin/python /Users/januswing/jupyterlab/mapCrawler/tasks/word2pdf.py ${filename}
# 
# echo "py执行成功......" >> ~/data/word2pdf.log
# ```
# 
# ### 2. 附上上述shell调用的py脚本，按需自行修改使用

# In[ ]:


from docx2pdf import convert
from pyzotero import zotero
import sys
import os
import re

def add_escape(value):
    reserved_chars = r'''?&|!{}[]()^~*:\\"'+ '''
    replace = ['\\' + l for l in reserved_chars]
    trans = str.maketrans(dict(zip(reserved_chars, replace)))
    return value.translate(trans)

if __name__ == '__main__':
    doc_file = sys.argv[1]
    ## Zotero接口参数
    library_id = ''
    library_type = ''
    api_key = ''

    doc_file_cmd = add_escape(doc_file)
    pdf_temp_path = '/Users/januswing/data/'
    tmp_symbol_loc = [each.start() for each in re.finditer("/", doc_file)]
    file_title = doc_file[tmp_symbol_loc[-1]+1:len(doc_file)-4]
    pdf_temp_name = '{}{}{}'.format(pdf_temp_path, file_title, 'pdf')
    pdf_temp_name_cmd = add_escape(pdf_temp_name)

    os.system('chmod 777 {}'.format(doc_file_cmd))
    os.system('rm -f {}'.format(pdf_temp_name_cmd))

    convert(doc_file, pdf_temp_name)
    # 连接 Zotero
    zot = zotero.Zotero(library_id, library_type, api_key)
    # 保存Zotero条目
    ## 请保证云存储空间充足
    template = zot.item_template('document')
    template['title'] = file_title
    res = zot.create_items([template])
    item_id = res['successful']['0']['key']
    attachment_path = pdf_temp_name
    zot.attachment_simple([attachment_path], item_id)


# In[ ]:




