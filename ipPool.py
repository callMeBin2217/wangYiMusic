__author__='callMeBin'
#-*-coding:utf-8-*-

'''
构建IP线程池，用于爬虫爬取
'''
import requests
from bs4 import BeautifulSoup
import random
import time

class ipPool(object):
	def __init__(self):
		self.base_url = r'http://www.xicidaili.com/nn/'
		self.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    	}
		self.ipList=[]


	#获取首页所有内容
	def getPage(self):
		req = requests.get(self.base_url,headers=self.headers)
		#print(req.text)
		return req.text


	#使用beautifulSoup获取所需内容
	def getIpList(self):
		data = self.getPage()
		soup = BeautifulSoup(data,'lxml')
		tr_list = soup.find_all('tr')
		for i in range(1,len(tr_list)):
			info_tr = tr_list[i]
			#print(info_tr)
			info_td = info_tr.find_all('td')
			tempUrl = str.lower(info_td[5].text)+'://'+info_td[1].text+':'+info_td[2].text
			#print(tempUrl)
			tempInfo = (str.lower(info_td[5].text),tempUrl) #返回样例 (http,http://192.168.1.1:80)
			#ipList.append(tempInfo)
			#print(ipList)
			if self.vaild_ip(tempUrl):
				self.ipList.append(tempInfo)
		return self.ipList


	#检测IP地址可用性
	def vaild_ip(self,ip):
		test_url = 'https://www.baidu.com'
		proxy = {'http': ip}
		#user_agent = random.choice(self.user_agent_list)
		#headers = {'User-Agent': user_agent}
		try:
			response = requests.get(test_url, headers=self.headers, proxies=proxy, timeout=5)
			#time.sleep(5)
			if response.status_code == 200:
				print('有用ip:'+str(ip))
				return True
			else:
				return False
		except Exception as e:
			print(e)
			return False




		#随机返回一个Ip
	def get_random_ip(self,ipList):
		#ipList = self.getIpList()
		pro = random.choice(ipList)
		proxies={pro[0]:pro[1]}
		return proxies



if __name__ == '__main__':
	spider = ipPool()
	ipList = spider.getIpList()
	proxies = spider.get_random_ip(ipList)
	print(proxies)

