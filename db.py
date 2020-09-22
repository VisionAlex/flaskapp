import pymysql.cursors


def connection():
	conn = pymysql.connect(host='34.65.195.156',
						   user='root',
						   password='Babadochia0@',
						   db='portfolio_tracker',
						   charset='utf8mb4',
						   cursorclass=pymysql.cursors.DictCursor)
	c = conn.cursor()
	return c, conn



