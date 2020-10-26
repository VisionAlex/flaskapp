from . import db
from .celery import celery_app
from .isin_code import get_data_from_isin
import csv
from datetime import datetime



@celery_app.task
def degiro_uploader(user_id,file,account_currency="EUR",base_currency="EUR"):
	with open(file) as f:
		reader = csv.DictReader(f)
		reader.fieldnames[6] = 'Currency'
		c, conn	= db.connection()
		for row in reader:
			date = datetime.strptime(' '.join([row['Date'], row['Time']]), "%d-%m-%Y %H:%M")
			isin = row['ISIN']
			currency = row['Currency']
			units = row['Quantity']
			query =c.execute("SELECT mic,exch_code,country FROM exchanges WHERE degiro = %s ",(row['Exchange']))
			if query:
				temp = c.fetchone()
				exchange = temp['mic']
				exch_code = temp['exch_code'] if temp['exch_code'] else temp['country']
				data = get_data_from_isin(isin, exchange_code=exch_code)
			else:
				exchange = None
			if exchange:
				data = get_data_from_isin(isin, exchange_code=exch_code)
			else:
				data = get_data_from_isin(isin)

			name = data['name'] if data else row['Product']
			symbol = data['ticker'] if data else None
			fx_rate = float(row['Exchange rate'])

			if currency != 'GBX':
				price = float(row['Price'])
			else:
				fx_rate = fx_rate/100
				price = float(row['Price'])/100
				currency = 'GBP'

			fee = float(row['Fee']) if row['Fee'] else 0
			if base_currency != account_currency: 
				conversion = ''.join([base_currency,account_currency])
				c.execute("SELECT * FROM fx_rates WHERE date_col = %s",(date.date()))
				rate = c.fetchone()[conversion]
				fx_rate = fx_rate * rate
				fee = fee / rate
			if symbol == '4GLD':
				asset_type = 'Gold'
			else:
				asset_type = 'Stocks'
			try:
				c.execute("INSERT INTO transactions (user_id, asset_type, date_col, symbol, name, units, price, currency, fx_rate, isin, exchange, fee, broker) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
					(user_id, asset_type, date, symbol, name, units, price, currency, fx_rate, isin, exchange, fee, 'DEGIRO'))
				conn.commit()
				print(f"{symbol} succesfully added")
			except Exception as e:
				conn.close()
				print(f"{isin} has error {e}")
		conn.close()
	return "Done"	


