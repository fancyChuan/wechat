# -*- encoding: utf-8 -*-

import json
import pymysql
from xml.etree import ElementTree as ET

import itchat
from itchat.content import *

#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')

def parse2dict(xml):
    data = ET.fromstring(xml)

def extract_all(msg):
    from_user_name = msg['FromUserName']
    to_user_name = msg['ToUserName']
    createtime = str(msg['CreateTime'])

    et = ET.fromstring(msg['Content'].encode('utf-8'))
    mp_name = ''
    for item in et.getiterator('publisher')[0].getchildren():
        if item.tag == 'nickname':
            mp_name = item.text

    data = []
    for item in et.getiterator('item'):
        d = dict([(x.tag, x.text) for x in item.getchildren()])
        title = d.get('title')
        url = d.get('url')
        data.append([mp_name, title, url, from_user_name, to_user_name, createtime])
    return data

def write2mysql(datas):
    conn = pymysql.connect(host='115.28.105.44', port=3306, user='fancy', password='fancyChuan',
                           charset='UTF8', database='monitor')
    cur = conn.cursor()
    sql = "insert into mpsharing(mp_name, title, url, from_user_name, to_user_name, createtime) VALUES(%s, %s, %s, %s, %s, %s)"
    cur.executemany(sql, datas)
    conn.commit()
    print '[%d] success to write to mysql' % len(datas)
    conn.close()


# 注册消息响应事件
@itchat.msg_register(SHARING, isMpChat=True)
def getMpSharing(msg):

    data = extract_all(msg)
    #print '=============='
    # print data
    #for d in data:
    #    print ', '.join(d)
    #print '-------'
    write2mysql(data)

itchat.auto_login(hotReload=True, enableCmdQR=2)

itchat.run(debug=True)
