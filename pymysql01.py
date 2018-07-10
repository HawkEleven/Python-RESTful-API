#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-07-06 14:30:10
# @Author  : Eleven (eleven.hawk@gmail.com)
# @Link    : https://github.com/HawkEleven
# @Version : 1.0

import pymysql
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json
from newBaseModel import NewBaseModel
import functools

class MySQLCommand(object):
    # 类的初始化
    def __init__(self):
        self.host = 'localhost'
        self.port = 3306  # 端口号
        self.user = 'root'  # 用户名
        self.password = "123"  # 密码
        self.db = "home"  # 库
        self.table = "home_list"  # 表
        self.insert_id = 0;

    # 链接数据库
    def connectMysql(self):
        try:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user,
                                        passwd=self.password, db=self.db, charset='utf8', cursorclass = pymysql.cursors.DictCursor)
            self.cursor = self.conn.cursor()
        except:
            print('connect mysql error.')

    def insertData(self, my_dict):
        table = self.table
        sqlExit = "SELECT url FROM home_list WHERE url = ' %s '" % (my_dict['url'])
        res = self.cursor.execute(sqlExit)
        if res:
            print('数据已存在', res)
            return 0

        try:
            cols = ', '.join(my_dict.keys())
            values = '","'.join(map(str, my_dict.values()))
            sql = "INSERT INTO home_list (%s) VALUES (%s)" % (cols, '"' + values + '"')
            try:
                result = self.cursor.execute(sql)
                # insert_id = self.conn.insert_id()
                self.conn.commit()
                if result:
                    self.insert_id += 1
                    print('插入成功 id = ', self.insert_id)
                    return self.insert_id
            except pymysql.Error as e:
                # 发生错误时回滚
                self.conn.rollback()
                # 主键唯一，无法插入
                if "KEY 'PRIMARY'" in e.args[1]:
                    print("数据已存在，未插入数据")
                else:
                    print("插入数据失败，原因 %d: %s" % (e.args[0], e.args[1]))
        except pymysql.Error as e:
            print("数据库错误，原因%d: %s" % (e.args[0], e.args[1]))

    def selectAllData(self):
        sql = "SELECT * FROM home_list ORDER BY id ASC"
        res = self.cursor.execute(sql)
        if res:
            return self.cursor.fetchall()

    def selectDataById(self, id):
        sql = "SELECT * FROM home_list WHERE id = '%s'" % (id)
        res = self.cursor.execute(sql)
        if res:
            print('数据存在')
            return self.cursor.fetchall()

    def getLastId(self):
        sql = "SELECT max(id) FROM " + self.table
        try:
            self.cursor.execute(sql)
            row = self.cursor.fetchone()  # 获取查询到的第一条数据
            if row[0]:
                return row[0]  # 返回最后一条数据的id
            else:
                return 0  # 如果表格为空就返回0
        except:
            print(sql + ' execute failed.')

    def closeMysql(self):
        self.cursor.close()
        self.conn.close()  # 创建数据库操作类的实例



Base = declarative_base()
class NewModel(Base):
    __tablename__ = 'home_list'
    
    id = Column(String(20))
    title = Column(String(20))
    img_path = Column(String(20))
    url = Column(String(20), primary_key=True)


class SqlalchemyCommand(object):
    # 初始化数据库连接:
    def connectMysql(self):
        engine = create_engine('mysql+mysqlconnector://root:123@localhost:3306/home')
        # 创建DBSession类型:
        DBSession = sessionmaker(bind=engine)
        # 创建session对象:
        self.session = DBSession()

    def selectAllData(self):
        results = self.session.query(NewModel).all()
        res = []
        for newModel in results:
            print(newModel.id)
            res.append(self._toDict(newModel)[0])
        return res

    def selectDataById(self, id):
        # order_by(NewModel.id.asc())排序函数
        newModel = self.session.query(NewModel).filter(NewModel.id==id).one()
        return self._toDict(newModel)
    
    def _toDict(self, newModel):
        model = NewBaseModel(newModel.id, newModel.title, newModel.img_path, newModel.url)
        json_str = json.dumps(model, default=lambda obj: obj.__dict__)
        # print(json_str)
        # print(json.loads(json_str))
        return [json.loads(json_str)]

    def closeMysql(self):
        self.session.close()

def createdatabase():
    db = pymysql.connect(host='localhost', port=3306, user='root', password='123')
    cursor = db.cursor()
    cursor.execute('SELECT VERSION()')
    data = cursor.fetchone()
    print('Database version:', data)
    cursor.execute("CREATE DATABASE home DEFAULT CHARACTER SET utf8")
    db.close()

def createtable():
    db = pymysql.connect(host='localhost', user='root', password='123', port=3306, db='home')
    cursor = db.cursor()
    sql = 'CREATE TABLE IF NOT EXISTS home_list (id int NOT NULL, title VARCHAR(255) NOT NULL, img_path VARCHAR(255) NOT NULL, url VARCHAR(255) NOT NULL, PRIMARY KEY (id))'
    cursor.execute(sql)
    db.close()

# createtable()
