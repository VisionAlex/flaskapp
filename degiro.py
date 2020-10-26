from . import db
from isin_code import get_data_from_isin
import csv
import logging
from datetime import datetime

logging.basicConfig(filename='/var/www/FlaskApp/instance/error.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')


def validate_csv(firstline):
	columns = firstline.split(',')
	for el in ['Date','Time','Product', 'ISIN', 'Exchange', 'Quantity', 'Exchange rate', 'Fee']:
		if el not in columns:
			return False
	if columns[6]:
		return False
	return True



	

