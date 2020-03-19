#!/user/bin/even python
# -*- coding:utf-8 -*-
import configparser
import logging
import sys

import pymysql
import requests
import time
import xlrd
import os

# 加入日志
# 获取logger实例
logger = logging.getLogger("baseSpider")
# 指定输出格式
formatter = logging.Formatter('%(asctime)s%(levelname)-8s:%(message)s')
# 文件日志
file_handler = logging.FileHandler("baseSpider.log")
file_handler.setFormatter(formatter)
# 控制台日志
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
# 为logge添加具体的日志处理器
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)

class downunicode():
    def __init__(self):
        cf = configparser.ConfigParser()
        # root_dir = "/home/work/conf/app_config.ini"
        root_dir = "C:\\Users\\Administrator\\Desktop\\辰星\\OriStart\\conf\\app_config.ini"
        cf.read(root_dir)
        self.rds_host = cf.get("bi_rds", "rds_host")
        self.rds_user = cf.get("bi_rds", "rds_user")
        self.rds_pwd = cf.get("bi_rds", "rds_pwd")
        self.rds_job = cf.get("bi_rds", "rds_job_db")
        self.username = cf.get("proxy", "proxy_user")
        self.password = cf.get("proxy", "proxy_pwd")
        self.api = cf.get("proxy", "proxy_host")
        self.db = pymysql.connect(self.rds_host, self.rds_user, self.rds_pwd, self.rds_job, charset='utf8')
        self.cursor = self.db.cursor()


    def downinfo(self):
        url=" https://zgdypw.cn/bits/w/films/pors/export?sort=id,desc"
        header={
        "Host":"zgdypw.cn",
        "Connection":"keep-alive",
        "Accept":"application/json, text/plain, */*",
        "Pragma":"no-cache",
        "Cache-Control":"no-cache",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        "Referer":"https://zgdypw.cn/",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"zh-CN,zh;q=0.9",
        }

        res=requests.get(url,headers=header)
        if res.status_code==200:
            if os.path.exists("./unicode.xls"):
                os.remove("./unicode.xls")
            with open ("./unicode.xls","wb") as res.raw:
                res.raw.write(res.content)  # 原始数据写入文件中
                print('文件下载成功！！')

    def readdata(self):
        is_data=[]
        sql="select movie_unicode from dim_movie_code"
        self.cursor.execute(sql)
        for each in self.cursor.fetchall():
            is_data.append(each[0])
        return is_data


    def writinfo(self,data):
        book = xlrd.open_workbook('./unicode.xls')
        sheet1 = book.sheets()[0]
        nrows = sheet1.nrows
        for i in range(1,nrows):
            row3_values = sheet1.row_values(i)
            if row3_values[1] not in data:
                print(row3_values)
                sql="insert into dim_movie_code(movie_unicode,movie_name,fabrication_style,detail_type,producer) VALUES('{}','{}','{}','{}','{}'); ".format(row3_values[1],row3_values[2],row3_values[3],row3_values[4],row3_values[5])
                self.cursor.execute(sql)
                self.db.commit()
        print("over")


    def run(self):
        star=time.time()
        print(star)
        self.downinfo()
        isdata=self.readdata()
        self.writinfo(isdata)
        print(star,time.time())


if __name__ =="__main__":
    coo=downunicode()
    coo.run()

