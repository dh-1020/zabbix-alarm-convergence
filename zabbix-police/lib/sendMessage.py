#/opt/Python-2.7.3/bin/python
# -*- coding: utf-8


from conf import zabbix
from conf import server
import urllib,urllib2
import json
import sys
import time

reload(sys)
sys.setdefaultencoding('utf-8')

class WechatSend:
    def gettoken(self):
        gurl = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=" + zabbix.cropid + "&corpsecret=" + zabbix.secret
        token_file = urllib2.urlopen(gurl)
        token_data = token_file.read().decode('utf-8')
        token_json = json.loads(token_data)
        token_json.keys()
        token = token_json['access_token']
        return token

    def send(self, user, content):
        access_token = self.gettoken()
        purl = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + access_token
        send_values = {
            "touser": user,    # 企业号中的用户帐号，在zabbix用户Media中配置，如果配置不正常，将按部门发送。
            # "toparty": "2",    # 企业号中的部门id
            "msgtype": "text",  # 消息类型
            "agentid": "1000003",  # 填写企业号中的应用id
            "text": {
                "content": content
            },
            "safe": "0"
        }

        send_data = json.dumps(send_values, ensure_ascii=False)
        send_request = urllib2.Request(purl, send_data)
        response = json.loads(urllib2.urlopen(send_request).read())

    def send_message(self, user, message):
        # 发送告警信息
        if message:
            self.send(user, message)
            currenttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

            with open(server.LogFile, 'a+') as write_f:
                write_f.write(currenttime + '\n' + message + '\n\n')
