import pymysql.cursors


def connection():
	conn = pymysql.connect(host='localhost',
						   user='visionalex',
						   password='burkinafaso46',
						   db='webapp',
						   charset='utf8mb4',
						   cursorclass=pymysql.cursors.DictCursor)
	c = conn.cursor()
	return c, conn



