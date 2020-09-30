from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, DecimalField, RadioField
from wtforms.validators import InputRequired

currencies = ['EUR','USD','GBP','RON','NOK','SEK','CAD']
asset_types = [('stocks','Stocks'), ('gold','Gold'), ('real_estate','Real Estate'), ('bonds','Bonds'), ('cash','Cash'),]

class TransactionsForm(FlaskForm):
	asset_type = SelectField('asset_type', choices=asset_types)
	buy_sell = SelectField('buy_sell', choices=["Buy", "Sell"])
	date = DateField('date',format='%Y-%m-%d')
	symbol = StringField('symbol')
	name = StringField('name')
	units = DecimalField('units')
	price = DecimalField('price')
	currency = SelectField('currency', choices=currencies)
	fx_rate = DecimalField("fx_rate")


