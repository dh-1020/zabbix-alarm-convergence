#/opt/Python-2.7.3/bin/python
# -*- coding: utf-8 -*-


import time


class Convergence:
    def __init__(self, all_originallist):
    	self.all_originallist = all_originallist
    
    def merge(self):
    	'''将数据库源数据triggerkey一样的合并成一组'''
    
    	triggerkey_list = []
    	originaldict = {}
    
    	for dic in self.all_originallist:
    	    if dic['triggerkey'] not in triggerkey_list:
    	        triggerkey_list.append(dic['triggerkey'])
    		originaldict[dic['triggerkey']] = []
    
    	for dic in self.all_originallist:
    	    for triggerkey in triggerkey_list:
    		if dic['triggerkey'] == triggerkey:
    	            originaldict[triggerkey].append(dic)
    
    	return originaldict
    
    def compress(self):
    	'''将同一个triggerkey报警信息压缩'''
    
    	merge_data = self.merge()
    	currenttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    	message_list = []
    
    	for key in merge_data:
            originalist = merge_data[key]
            ipaddress = ''
            itmes = ''
            triggerstatus = ''
            item_values = ''
            
            # 获取报警信息的IP地址
            for dic in originalist:
            	ip = dic['ipaddress'].strip('\r\n')
                value = dic['itemvalue'].strip('\r\n')
            
            	if ip not in ipaddress:
            	    ipaddress +=  ip + ' '
            
                if value not in item_values:
		    item_values += value + ' '

            	itmes = dic['triggeritems'].strip('\r\n')
            	triggerstatus = dic['triggerstatus'].strip('\r\n')
            
            message = '报警状态: ' + triggerstatus + '\n' '报警主机: ' + ipaddress + '\n' + '报警项目: ' + itmes + '\n' + '报警时间: ' + currenttime + '\n' + 'item当前值: ' + item_values
            message_list.append(message)
    
	return '\n\n'.join(message_list)
