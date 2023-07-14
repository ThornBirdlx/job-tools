#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/7/11 20:34
# @Author : LiuXiu
import sys

from flask import Flask, request, send_file
import os
import pandas as pd

app = Flask(__name__)

app.config['SERVER_NAME'] = 'localhost:9997'  # 指定监听端口为5000
# new_filename =""

@app.route('/')
def index():
    return '''
        <html>
            <body>
                <h1>文件上传和下载</h1>
                <form method="POST" action="/upload" enctype="multipart/form-data">
                    <input type="file" name="file">
                    <input type="submit" value="上传">
                </form>
            </body>
        </html>
    '''


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        new_filename = filename.rsplit(".", 1)[0] + ".xlsx"

        # 读取csv文件
        df = pd.read_csv(file)
        # 复制指定列数据
        new_df = pd.DataFrame()
        new_df['联系电话'] = df['c_code']
        new_df['brand'] = df['brand']
        new_df['mkt_id'] = df['mkt_id']
        new_df['loop_id'] = df['loop_id']
        new_df['node_id'] = df['node_id']

        # 将结果输出到excel文件
        new_df.to_excel(new_filename, index=False)
        # # 设置生成的结果文件路径
        # result_filename = 'new_data.xlsx'

        return '''
            <html>
                <body>
                    <h1>文件下载</h1>
                    <a href="/download">下载结果文件</a>
                </body>
            </html>
        '''


# 获取程序运行时的绝对路径
basedir = os.path.abspath(os.path.dirname(sys.argv[0]))


@app.route('/download')
def download():
    # 设
    # 置生成的结果文件路径
    # result_filename = 'result.xlsx'
    # 设置生成的结果文件路径为相对路径
    result_filename = os.path.join(basedir, new_filename)
    # 检查文件是否存在
    if not os.path.exists(result_filename):
        return "文件不存在"

    # 以附件形式下载
    return send_file(result_filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
