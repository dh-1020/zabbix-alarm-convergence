#/opt/Python-2.7.3/bin/python
# -*- coding: utf-8 -


from conf import mysql
from conf import server
import MySQLdb


#定义通过actionid和subject获取数据库告警具体信息，并以字典形式返回
def alerts_eventid(actionid,subject):
    try:
        # Mysql Zabbix数据库连接信息
        conn = MySQLdb.connect(host=mysql.host, user=mysql.user, passwd=mysql.password, db=mysql.db, port=mysql.port)
        cursor = conn.cursor()
        cursor.execute("SET NAMES utf8");
        sql = "SELECT * FROM alerts where actionid = '%s' and subject = '%s' ;" % (actionid, subject)
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        event = data[0]
        messagelist = []
        message = event[8]
        messageone = message.split('#')

        for i in messageone:
                messagelist.append(i.split('|'))

        messagedict = dict(messagelist)

        return messagedict
    except MySQLdb.Error as e:
        with open(server.LogFile, 'a+') as write_f:
            write_f.write("Mysql Error %d: %s" % (e.args[0], e.args[1]))
