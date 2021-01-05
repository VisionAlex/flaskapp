import pymysql.cursors


def connection():
	conn = pymysql.connect(host='',
						   user='',
						   password='',
						   db='',
						   charset='utf8mb4',
						   cursorclass=pymysql.cursors.DictCursor)
	c = conn.cursor()
	return c, conn



