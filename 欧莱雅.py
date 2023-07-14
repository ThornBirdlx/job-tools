#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/7/14 11:12
# @Author : LiuXiu
import os
import pandas as pd
from flask import Flask, request, send_file

app = Flask(__name__)
app.config['SERVER_NAME'] = 'localhost:9996'  # 指定监听端口为5000

@app.route('/')
def index():
    return '''
        <html>
            <body>
                <h1>文件上传和处理</h1>
                <form method="POST" action="/upload" enctype="multipart/form-data">
                    <input type="file" name="file">
                    <input type="submit" value="上传">
                </form>
            </body>
        </html>
    '''

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    filename = file.filename

    # 保存上传的文件到本地
    file_path = os.path.join(app.root_path, filename)
    file.save(file_path)

    # 读取上传的 CSV 文件
    df = pd.read_csv(file_path)

    # 处理数据...
    # 复制指定列数据
    new_df = pd.DataFrame()
    new_df['联系电话'] = df['c_code']
    new_df['brand'] = df['brand']
    new_df['mkt_id'] = df['mkt_id']
    new_df['loop_id'] = df['loop_id']
    new_df['node_id'] = df['node_id']
    # 生成 XLSX 文件
    xlsx_filename = os.path.splitext(filename)[0] + '.xlsx'
    xlsx_file_path = os.path.join(app.root_path, xlsx_filename)
    new_df.to_excel(xlsx_file_path, index=False)

    return '''
        <html>
            <body>
                <h1>处理完成</h1>
                <a href="/download">下载结果文件</a>
            </body>
        </html>
    '''

@app.route('/download')
def download():
    xlsx_filename = None  # 存储要下载的文件名（默认为空）
    for filename in os.listdir(app.root_path):
        if filename.endswith('.xlsx'):
            xlsx_filename = filename
            break

    if xlsx_filename is None:
        return "文件不存在"

    xlsx_file_path = os.path.join(app.root_path, xlsx_filename)
    return send_file(xlsx_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run()
