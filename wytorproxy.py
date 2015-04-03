#!/usr/bin/env python
# encoding: utf-8
# file: torproxy.py
# mail: ringzero@0x557.org

import sys
import random
import requests
import json

# 动态配置项
retrycnt = 3	# 重试次数
timeout = 10	# 超时时间

# 动态使用代理，为空不使用，支持用户密码认证
proxies = {
	# "http": "http://user:pass@10.10.1.10:3128/",
	# "https": "http://10.10.1.10:1080",
	"http": "http://127.0.0.1:8118", # TOR 洋葱路由器
}
result = {}

# 随机生成User-Agent
def random_useragent():
	USER_AGENTS = [
		"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
		"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
		"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
		"Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
		"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
		"Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
		"Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
		"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
		"Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
		"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
		"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
		"Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
		"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
		"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
	]
	return random.choice(USER_AGENTS)

# 随机X-Forwarded-For，动态IP
def random_x_forwarded_for():
	return '%d.%d.%d.%d' % (random.randint(1, 254),random.randint(1, 254),random.randint(1, 254),random.randint(1, 254))

def http_request_get(url, body_content_workflow=0):
	trycnt = 0
	# cookies = dict(scan_worker='working', cookies_be='wscan.net')
	headers = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20',
		'Referer' : url,
		'Cookie': 'whoami=wytorproxy',
		}
	while True:
		try:
			if body_content_workflow == 1:
				result = requests.get(url, stream=True, headers=headers, timeout=timeout, proxies=proxies)
				return result
			else:
				result = requests.get(url, headers=headers, timeout=timeout, proxies=proxies)
				return result
		except Exception, e:
			# print 'Exception: %s' % e
			trycnt += 1
			if trycnt >= retrycnt:
				# print 'retry overflow'
				return False

def http_request_post(url, payload, body_content_workflow=0):
	'''
		payload = {'key1': 'value1', 'key2': 'value2'}
	'''
	trycnt = 0
	# cookies = dict(scan_worker='working', cookies_be='wscan.net')
	headers = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20',
		'Referer' : url,
		'Cookie': 'whoami=wytorproxy',
		}
	while True:
		try:
			if body_content_workflow == 1:
				result = requests.post(url, data=payload, headers=headers, stream=True, timeout=timeout, proxies=proxies)
				return result
			else:
				result = requests.post(url, data=payload, headers=headers, timeout=timeout, proxies=proxies)
				return result
		except Exception, e:
			# print 'Exception: %s' % e
			trycnt += 1
			if trycnt >= retrycnt:
				# print 'retry overflow'
				return False

def check_website_status(url):
	result = http_request_get(url, body_content_workflow=1)
	if result == False:
		# 服务器宕机或者选项错误
		return {'status': False, 'info': 'server down or options error'}
	elif result.status_code != requests.codes.ok:
		# 返回值不等于200
		result_info = 'status_code: %s != 200' % result.status_code
		return {'status': False, 'info': result_info}
	else:
		# 返回正常
		return {'status': True, 'info': 'response ok'}

print http_request_get('http://ip.taobao.com/service/getIpInfo2.php?ip=myip').text


