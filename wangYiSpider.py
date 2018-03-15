__author__='callMeBin'
#-*-coding:utf-8-*-
'''
目标：爬取网易云音乐评论，储存到数据库中
'''
import requests
import getpass
import encrypTools
import dataBaseTool
import json
import chardet
import time

class wangYiSpider(object):
	def __init__(self,id):
		#初始化一个commentList爬取存下来的评论
		self.commentList =[]
		self.count = 1
		self.sys_name = getpass.getuser()
		self.modulus = r'00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
		self.nonce = r'0CoJUm6Qyw8W8jud'
		self.pubKey = '010001'
		self.encryptTool = encrypTools.encrypTools()
		self.secKey = self.encryptTool.createSecretKey(16)
		#一、生成16位密钥；二、进行RSA加密
		self.encSecKey = self.encryptTool.rsaEncrypt(self.secKey,self.pubKey,self.modulus)
		self.musicId = id
		self.BASE_URL = r"http://music.163.com/weapi/v1/resource/comments/R_SO_4_%d/"%int(self.musicId)
		self.headers = {
			'Host':'music.163.com',
			'Connection':'keep-alive',
			'Content-Length':'530',
			'Cache-Control':'max-age=0',
			'Origin':'http://music.163.com',
			'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
			'Content-Type':'application/x-www-form-urlencoded',
			'Accept':'*/*',
			'DNT':'1',
			'Accept-Encoding':'gzip,deflate',
			'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
			'Cookie':r'__e_=1515631791549; _ntes_nnid=c88c078d22d8515e624ea4e5db7e2e0d,1515631791598; _ntes_nuid=c88c078d22d8515e624ea4e5db7e2e0d; __gads=ID=db5bcf91a4f4474a:T=1516954068:S=ALNI_MbOfciBUKkaPIihHY6CmzO6fTs5vQ; UM_distinctid=161318220f3496-0d23e92b7b7267-5d4e211f-1fa400-161318220f4711; vjuids=9a46435bb.16131822360.0.62cca3f22db48; vjlast=1516954068.1516954068.30; vinfo_n_f_l_n3=fd7c70cc0e58e199.1.0.1516954067832.0.1516954082832; usertrack=ezq0pVp4IaO0pxVxA0tGAg==; _ga=GA1.2.351628758.1517822370; JSESSIONID-WYYY=QEN5%2FvapXy7fhzq%5C8VwUDxPE7RNxg4zul3FdSRE4vbrnI1%2F%2BfFe9kHmbMcAz3pVTo7Nz550p8SdVC%5CvH6%2Bnzes5OlRok8tuVDpT%2FAimyEVhrqKqHgpx24%2BUQGw74o2JEIjVoPiDBWaivmlMESrnc%2BVW%2BWweta92Q307Su2UYHX03AmsD%3A1521016110455; _iuqxldmzr_=32; __utma=94650624.351628758.1517822370.1520214948.1521012276.12; __utmb=94650624.15.10.1521012276; __utmc=94650624; __utmz=94650624.1521012276.12.10.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; MUSIC_U=0cecdd66b7edc1a99a72906bb5549fb751236a4e96104851cc1f090d8edc110c0c18a949e593acaceebd224a0aaa3eeade39c620ce8469a8; __remember_me=true; __csrf=01b4286878646905fbb124b6a3f49112'

		}
		self.dbTool = dataBaseTool.dataBaseTool()


	#获取评论，传入评论与偏移量参数到方法saveToDB
	def getComment(self,offset):
		#构造需要的文本
		text ={
			'username':'',
			'password':'',
			'rememberLogin':'true',
			'offset': offset
		}
		text = json.dumps(text)
		#对文本进行两次 AES加密
		encText = self.encryptTool.aesEncrypt(self.encryptTool.aesEncrypt(text,self.nonce).decode('utf-8'),self.secKey)
		data = {
			'params':encText,
			'encSecKey':self.encSecKey
		}
		recq = requests.post(self.BASE_URL,headers=self.headers,data=data)
		jsonData = recq.json()
		#print(jsonData)
		try:
			print("进入try")
			self.saveToDB(jsonData,offset)
			return int(jsonData['total'])
		except Exception as e:
			raise e


	#保存评论到数据库
	def saveToDB(self,jsonData,offset):
		print("进入savetodb")
		try:
			for c in jsonData['comments']:
				timeStr = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
				insert_str = "INSERT INTO comment(cnt,musicId,offset,insertTime)VALUES('%s','%s','%d','%s')"% (c['content'].strip(),self.musicId,offset,timeStr)
				print("正在插入")
				self.dbTool.execute_insert(insert_str)
		except Exception as e:
			raise e


	#控制爬取进度，在此添加一个断点续存
	def process(self,offset=1):
		if offset == -1:
			return
		#查询数据库最后一次查询offset是多少
		sql_str = "SELECT MAX(offset) as offset FROM COMMENT WHERE musicId='%s'"%(self.musicId)
		tempExe = self.dbTool.execute_one(sql_str)
		if tempExe['offset'] == None:
			print(offset)
			off = 1
		else:
			off = tempExe['offset']
			print(tempExe)
		#off = offset
		total = self.getComment(off)
		print('评论的总数'+str(total))
		while off <30:
			off+=10
			time.sleep(3)
			self.getComment(off)


def main(id='65546'):
	spider = wangYiSpider(id)
	spider.process(1)

if __name__ =='__main__':
	main('526464293')



