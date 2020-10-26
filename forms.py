from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SelectField, DateField, DecimalField, RadioField, SubmitField
from wtforms.validators import InputRequired

CURRENCIES = ['EUR','USD','GBP','RON','NOK','SEK','CAD']
ASSET_TYPES = ['Stocks','Gold','Real Estate', 'Bonds', 'Cash']
BROKERS = ['DEGIRO']

class TransactionsForm(FlaskForm):
	asset_type = SelectField('asset_type', choices=ASSET_TYPES)
	buy_sell = SelectField('buy_sell', choices=["Buy", "Sell"])
	date = DateField('date',format='%Y-%m-%d')
	symbol = StringField('symbol')
	name = StringField('name')
	units = DecimalField('units')
	price = DecimalField('price')
	currency = SelectField('currency', choices=CURRENCIES)
	fx_rate = DecimalField("fx_rate")
	fee = DecimalField("fee")
	submit1 =SubmitField('submit1')


class UploadFile(FlaskForm):
	broker = SelectField('broker', choices=BROKERS)
	account_currency = SelectField('account_currency', choices=CURRENCIES)
	file = FileField('upload', validators=[FileRequired(), FileAllowed(['csv'], message="Only CSV format suported.")])
	submit2 =SubmitField('submit2')