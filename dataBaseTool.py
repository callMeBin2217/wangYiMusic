__author__='callMeBin'
#-*-coding:utf-8-*-
'''
数据库工具类
1.建立连接 
2.获取游标 
3.执行语句 
4.提交结果(insert，update，delete) 
5.关闭游标 
6.关闭链接
'''

import pymysql

class dataBaseTool(object):
	def __init__(self):
		#初始化数据库常用配置
		self.host = r'localhost'
		self.user = r'root'
		self.password = r'1234' 
		self.db = r'commentdb'
		self.charset='utf8mb4'
		self.conn = None

	#查询所有,返回list
	def execute(self,sql_str):
		if sql_str is None or len(sql_str)==0:
			raise Exception("参数不能为空")
		try:
			#链接
			self.conn = pymysql.connect(host=self.host,user=self.user,password=self.password,db=self.db,charset=self.charset)
			with self.conn.cursor() as cursor:
				#执行
				cursor.execute(sql_str)
				data = cursor.fetchall()
				return data
		except Exception as e:
			raise e
		finally:
			self.conn.close()


	#插入数据
	def execute_insert(self,insert_sql):
		if insert_sql is None or len(insert_sql)==0:
			raise Exception("参数不能为空")
		try:
			self.conn = pymysql.connect(host=self.host,user=self.user,password=self.password,db=self.db,charset=self.charset)
			with self.conn.cursor() as cursor:
				cursor.execute(insert_sql)
			#提交修改到数据库
			self.conn.commit()
			print('提交成功')
		except Exception as e:
			#出现错误就回滚
			self.conn.rollback()
			raise e
		finally:
			self.conn.close()

	#查询单条信息
	def execute_one(self,sql_str):
		if sql_str is None or len(sql_str)==0:
			raise Exception("参数不能为空")
		try:
			#链接
			self.conn = pymysql.connect(host=self.host,user=self.user,password=self.password,db=self.db,charset=self.charset)
			with self.conn.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
				#执行
				cursor.execute(sql_str)
				data = cursor.fetchone()
				print(data)
				return data
		except Exception as e:
			raise e
		finally:
			self.conn.close()		