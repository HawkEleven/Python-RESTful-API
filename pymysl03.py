#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-07-06 16:11:33
# @Author  : Eleven (eleven.hawk@gmail.com)
# @Link    : https://github.com/HawkEleven
# @Version : 1.0
# api开发

from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import url_for
from flask.ext.httpauth import HTTPBasicAuth

from pymysql01 import MySQLCommand
from pymysql01 import SqlalchemyCommand


auth = HTTPBasicAuth()

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)

app = Flask(__name__)

mysqlCommand = MySQLCommand()
mysqlCommand.connectMysql()
news = mysqlCommand.selectAllData()

# news
@app.route('/news/api/v1.0/list', methods=['GET'])
def get_news():
    return jsonify({'news': news})

# news_id
@app.route('/news/api/v1.0/list/<int:new_id>', methods=['GET'])
def get_new(new_id):
   new = mysqlCommand.selectDataById(new_id)
   
   if new:
     return jsonify({'new': new[0]})
   else:
    abort(404)

# 404
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    # 默认监听localhost
    app.run(debug=True) 
    
    # # 可改为本地IP，在局域网供手机访问
    # app.run(host='电脑IP', port=8080, debug=True)
    
