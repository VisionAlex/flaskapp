import yfinance as yf
from sqlalchemy import create_engine
import pymysql

ticker = yf.Ticker('GC=F')
hist = ticker.history(period='1d', interval='1m')
last= hist.tail()['Close'].iloc[0]
print(last)

# host = '34.65.195.156'
# user = 'root'
# password = 'Babadochia0@'
# db = 'portfolio_tracker'
# charset = 'utf8mb4'

# engine =create_engine(f'mysql+pymysql://{user}:{password}@{host}/{db}')
# con = engine.connect()

# try:
# 	hist.to_sql(con=con, name='currentgold_prices', if_exists='replace')
# 	print('Gold prices updated successfully')
# except Exception as e:
# 	print(e)
# finally:
# 	con.close()
