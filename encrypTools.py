__author__='callMeBin'
#-*-coding:utf-8-*-

'''
目标：网易云音乐对获取的URL做了加密处理，需要把相关信息加密
  	  才能获取正确的JSON文件

  	  根据知乎大神的分析，可以知道用了两层加密(一：文本+私钥 as A，
  	  二:A as B)
'''

import base64
from Crypto.Cipher import AES
import json
import os
import codecs
import time

class encrypTools():
	def __init__(self):
		pass

	def createSecretKey(self,size=16):
		return (''.join(map(lambda xx:(hex(ord(xx))[2:]),str(os.urandom(size)))))[0:size]

	#进行AES加密
	def aesEncrypt(self,text,secKey):
		pad = 16 -len(text)%16
		text = text +pad*chr(pad)
		encryptor = AES.new(secKey,2,'0102030405060708')
		ciphertext = encryptor.encrypt(text)
		ciphertext = base64.b64encode(ciphertext)
		return ciphertext

	#进行RSA加密
	def rsaEncrypt(self,text,pubKey,modulus):
		text = text[::-1]
		tempHex = codecs.encode(text.encode('utf-8'),'hex')
		rs = int(tempHex,16)**int(pubKey,16)%int(modulus,16)
		return format(rs,'x').zfill(256)

	#生成时间戳
	def timeStamp(self,timeNum):
		time_stamp = float(timeNum/1000)
		time_array = time.localtime(time_stamp)
		reTime = time.strftime("%Y-%m-%d %H:%M:%S",time_array)

