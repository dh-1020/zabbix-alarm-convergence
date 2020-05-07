#/opt/Python-2.7.3/bin/python
# -*- coding: utf-8 -*-


from lib import operation as op
from lib import dbread 
from lib import sendMessage
from conf import zabbix
from conf import RedisServer
import redis


class Datamerge:
    def __init__(self):
        self.zabbix_actionid = zabbix.actionid 
        self.redis_host = RedisServer.host
        self.redis_port = RedisServer.port
        self.redis_passwd = RedisServer.password
        self.redis_connect = redis.StrictRedis(host=self.redis_host, port=self.redis_port, password = self.redis_passwd)
        
    def get_source_data(self):
        '''获取数据库源数据并分析为问题信息和恢复信息'''

    	# 获取redis所有key并删除
        subjectlist = self.redis_connect.keys()
        
        if not subjectlist:
            exit()

        for i in subjectlist:
            self.redis_connect.delete(i)

        problem_originallist, normal_originallist = [], []

        # 获取数据库原始数据
        for subject in subjectlist:
                data = dbread.alerts_eventid(str(self.zabbix_actionid), subject)
                # {EVENT.ID_1}为报警信息 {EVENT.ID_0}为恢复信息
                if subject[-1] == '1':
                    problem_originallist.append(data)
                else:
                    normal_originallist.append(data)

        return problem_originallist, normal_originallist

    def operation(self):
        problem_originallist, normal_originallist = self.get_source_data()

        conv1 = op.Convergence(problem_originallist)
        conv2 = op.Convergence(normal_originallist)

        comp_data = conv1.compress()
        comp_data2 = conv2.compress()

        send = sendMessage.WechatSend()

        send.send_message(zabbix.user, comp_data)
        send.send_message(zabbix.user, comp_data2)
