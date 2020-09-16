import pymysql

connection =pymysql.connect(host='localhost',
							user='visionalex',
							password='burkinafaso46',
							db='webapp',
							cursorclass=pymysql.cursors.DictCursor
			)


c = connection.cursor()

sql = """CREATE TABLE `users` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `email` varchar(255) NOT NULL,
    `password` varchar(255) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB;"""

c.execute(sql)
c.commit()
c.close()