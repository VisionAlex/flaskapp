import pymysql.cursors


def connection():
	conn = pymysql.connect(host='graurului.tplinkdns.com',
						   user='',
						   password='',
						   db='',
						   charset='utf8mb4',
						   cursorclass=pymysql.cursors.DictCursor)
	c = conn.cursor()
	return c, conn



