const asset_type = document.querySelector("#asset_type")
const symbol = document.querySelector("#symbol")
const name = document.querySelector("#name")
const units = document.querySelector("#units")
const price = document.querySelector("#price")
const currency = document.querySelector("#currency")
const fx_rate = document.querySelector("#fx_rate")
const fx_help = document.querySelector("#fx_help")

asset_type.onchange = function() {
	if (asset_type.value == "Cash") {
		symbol.hidden = true;
		name.hidden = true;
		units.placeholder = "Amount";
		price.placeholder = "FX Rate";

	} else if (asset_type.value == "Real_Estate") {
		symbol.hidden = false;
		name.hidden = false;
		units.hidden = true;
		price.placeholder="Price";
	} else if (asset_type.value == "Gold") {
		symbol.hidden = false;
		symbol.placeholder = "Unit type(g, oz, paper)"
		name.hidden = true;
		units.hidden = false;
		price.placeholder = "Price"
		units.placeholder = "Units"

	} else if (asset_type.value == "Stocks") {
		symbol.hidden= false;
		symbol.placeholder = "Symbol"
		symbol.required = true;
		name.hidden=false;
		units.hidden = false;
		units.placeholder = "Shares"
		price.placeholder = "Price"
	} else if (asset_type.value == "bonds") {
		units.placeholder = "Units"
		symbol.hidden = false;
		symbol.placeholder = "Symbol"
		name.hidden = false;
		units.hidden = false;
	}	
}

currency.onchange = function() {
	if (currency.value != "EUR") {
		fx_rate.hidden = false;
		fx_help.hidden = false;
	} else {
		fx_rate.hidden = true;
		fx_help.hidden = true;
	}
}