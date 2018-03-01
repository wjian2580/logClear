#!/usr/bin/python
# coding: utf-8

import os
import yaml
import time
import re
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from datetime import datetime,timedelta
import pdb



#筛选符合要求的日志
def log_select(log):
#	exclude_files = config_parse('exclude_files')
#	if log in exclude_files:
#		return False
	keep = config_parse('keep')
	regx = r'[a-z.-_]+(\d{4}\-\d{2}\-\d{2})[a-z.-]?'
	matched = re.match(regx,log)
	if matched:
		date = matched.groups()[0]
		time = datetime.strptime(date,'%Y-%m-%d').date()
		return (time + timedelta(keep) <= datetime.now().date())
	return True


#解析配置文件
def config_parse(item):
	with open('/home/wanghailong3/a/log.yml',encoding='utf-8') as y:
		config = yaml.load(y)
	if config.get(item):
		return config[item]
	else:
		raise KeyError('配置项：%s不存在'% item)

def tomcat_restart():
	path = config_parse('catalina_home')
	script = os.path.join(path,'bin/restart.sh')
	if os.popen('sh %s' % script).readlines()[-1] == 'Tomcat started.\n':
		print('启动成功')
	else:
		pass


def send_mail():
	email = config_parse('email')
	from_addr,to_addr,smtp_server,port,password = [email[i] for i in email]

	msg['From'] = from_addr
	for receiver in to_addr:
		msg['To'] = receiver
	msg = MIMEText('请检查tomcat', 'plain', 'utf-8')
	msg['Subject'] = Header('tomcat启动失败', 'utf-8').encode()

	server = smtplib.SMTP(smtp_server, port)
	server.login(from_addr, password)
	server.sendmail(from_addr, [to_addr], msg.as_string())
	server.quit()


#主函数：删除日志
def main():
	log_paths = config_parse('log_path')
	for log_path in log_paths:
		if os.path.exists(log_path):
			logs = os.listdir(log_path)
			logs_to_clear = list(filter(log_select,logs))
			for log in logs_to_clear: 
				log_file = os.path.join(log_path,log)
				print('删除 %s' % log_file)
				os.remove(log_file)
		else:
			print('目录不存在: %s' % log_path)
	tomcat_restart()


if __name__ == '__main__':
	main()







	
