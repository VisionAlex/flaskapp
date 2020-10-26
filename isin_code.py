import openfigi

API_KEY = "1571ca02-11aa-462f-be9a-b6f00bd569a8"

def get_data_from_isin(isin_code, **kwargs):
	conn = openfigi.OpenFigi(API_KEY)
	try:
		conn.enqueue_request(id_type="ID_ISIN", id_value=isin_code, **kwargs)	
		data = conn.fetch_response()[0]
		if 'data' in data:
			return data['data'][0]
		if 'error' in data:
			conn.enqueue_request(id_type="ID_ISIN", id_value=isin_code)
			data = conn.fetch_response()[1]
			if 'data' in data:
				return data['data'][0]
			if 'error' in data:
				print(data['error'])	
				return None
		
	except Exception as e:
		print("ERROR")
		print(e)


if __name__ == '__main__':
	isin_code='US55315J1025'
	data = get_data_from_isin(isin_code, exchange_code="LN")
	print(data)