#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import json
import subprocess
from pathlib import Path
from tqdm.auto import tqdm

try:
    # 3.8+
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version

__version__ = version(__package__)


def windows(paths, keep_active):
    import win32com.client

    word = win32com.client.Dispatch("Word.Application")
    wdFormatPDF = 17

    if paths["batch"]:
        for docx_filepath in tqdm(sorted(Path(paths["input"]).glob("[!~]*.doc*"))):
            pdf_filepath = Path(paths["output"]) / (str(docx_filepath.stem) + ".pdf")
            doc = word.Documents.Open(str(docx_filepath))
            doc.SaveAs(str(pdf_filepath), FileFormat=wdFormatPDF)
            doc.Close(0)
    else:
        pbar = tqdm(total=1)
        docx_filepath = Path(paths["input"]).resolve()
        pdf_filepath = Path(paths["output"]).resolve()
        doc = word.Documents.Open(str(docx_filepath))
        doc.SaveAs(str(pdf_filepath), FileFormat=wdFormatPDF)
        doc.Close(0)
        pbar.update(1)

    if not keep_active:
        word.Quit()


def macos(paths, keep_active):
    script = "/Users/januswing/jupyterlab/docx2pdf/docx2pdf/convert.jxa"
    cmd = [
        "/usr/bin/osascript",
        "-l",
        "JavaScript",
        str(script),
        str(paths["input"]),
        str(paths["output"]),
        str(keep_active).lower(),
    ]

    def run(cmd):
        process = subprocess.Popen(cmd, stderr=subprocess.PIPE)
        while True:
            line = process.stderr.readline().rstrip()
            if not line:
                break
            yield line.decode("utf-8")

    total = len(list(Path(paths["input"]).glob("*.doc*"))) if paths["batch"] else 1
    pbar = tqdm(total=total)
    for line in run(cmd):
        print('line:', line)
        try:
            msg = json.loads(line)
        except ValueError as e:
            print('error:',e)
            continue
        if msg["result"] == "success":
            pbar.update(1)
        elif msg["result"] == "error":
            print(msg)
            sys.exit(1)


def resolve_paths(input_path, output_path):
    input_path = Path(input_path).resolve()
    output_path = Path(output_path).resolve() if output_path else None
    output = {}
    if input_path.is_dir():
        output["batch"] = True
        output["input"] = str(input_path)
        if output_path:
            assert output_path.is_dir()
        else:
            output_path = str(input_path)
        output["output"] = output_path
    else:
        output["batch"] = False
        assert str(input_path).endswith((".docx", ".DOCX", ".doc", ".DOC"))
        output["input"] = str(input_path)
        if output_path and output_path.is_dir():
            output_path = str(output_path / (str(input_path.stem) + ".pdf"))
        elif output_path:
            assert str(output_path).endswith(".pdf")
        else:
            output_path = str(input_path.parent / (str(input_path.stem) + ".pdf"))
        output["output"] = output_path
    return output


def convert(input_path, output_path=None, keep_active=False):
    paths = resolve_paths(input_path, output_path)
    if sys.platform == "darwin":
        return macos(paths, keep_active)
    elif sys.platform == "win32":
        return windows(paths, keep_active)
    else:
        raise NotImplementedError(
            "docx2pdf is not implemented for linux as it requires Microsoft Word to be installed"
        )


def cli():

    import textwrap
    import argparse

    if "--version" in sys.argv:
        print(__version__)
        sys.exit(0)

    description = textwrap.dedent(
        """
    Example Usage:

    Convert single docx file in-place from myfile.docx to myfile.pdf:
        docx2pdf myfile.docx

    Batch convert docx folder in-place. Output PDFs will go in the same folder:
        docx2pdf myfolder/

    Convert single docx file with explicit output filepath:
        docx2pdf input.docx output.docx

    Convert single docx file and output to a different explicit folder:
        docx2pdf input.docx output_dir/

    Batch convert docx folder. Output PDFs will go to a different explicit folder:
        docx2pdf input_dir/ output_dir/
    """
    )

    formatter_class = lambda prog: argparse.RawDescriptionHelpFormatter(
        prog, max_help_position=32
    )
    parser = argparse.ArgumentParser(
        description=description, formatter_class=formatter_class
    )
    parser.add_argument(
        "input",
        help="input file or folder. batch converts entire folder or convert single file",
    )
    parser.add_argument("output", nargs="?", help="output file or folder")
    parser.add_argument(
        "--keep-active",
        action="store_true",
        default=False,
        help="prevent closing word after conversion",
    )
    parser.add_argument(
        "--version", action="store_true", default=False, help="display version and exit"
    )

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    else:
        args = parser.parse_args()

    convert(args.input, args.output, args.keep_active)


# In[24]:


doc_file = '/Users/januswing/Nutstore Files/projects/doc_智慧港口建设指南/智慧港口-素材汇总/04-港口数字基础-基础支撑平台/数字孪生港口(散货)建设工程-20220701.docx'
pdf_temp_name = '/Users/januswing/data/04-港口数字基础-基础支撑平台/数字孪生港口(散货)建设工程-20220701.pdf'
convert(doc_file, pdf_temp_name)


# In[4]:


from docx2pdf import convert
from pyzotero import zotero
import sys
import os
import re

## Zotero接口参数
library_id = '5012819'
library_type = 'user'
api_key = 'FkXpNmTlLwqDnhKxS2n2zgoj'
# 连接 Zotero
zot = zotero.Zotero(library_id, library_type, api_key)
# 保存Zotero条目
## 请保证云存储空间充足
template = zot.item_template('document')
template['title'] = 'test_ntimes'
res = zot.create_items([template])
item_id = res['successful']['0']['key']
attachment_path = '/Users/januswing/data/doctest.pdf'
res = zot.attachment_simple([attachment_path], item_id)


# In[10]:


attachment_key = res['success'][0]['key']


# In[20]:


sync_path = '/Users/januswing/Zotero/storage/{}'.format(attachment_key)
os.system('mkdir {}'.format(sync_path))
os.system('cp {} {}/'.format(attachment_path,sync_path))


# In[12]:


attachment_path


# In[14]:


attachment_key


# In[15]:


sync_path


# In[18]:


print('cp {} {}/'.format(attachment_path,sync_path))


# In[ ]:


zot.upload_attachments(['doctest.pdf'],item_id,'/Users/januswing/data')


# In[ ]:


zot.upload_attachments(attachment_path, [item_id])


# In[ ]:




