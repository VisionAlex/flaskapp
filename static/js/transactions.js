let asset_type = document.getElementById("asset_type")
let symbol = document.getElementById("symbol")
let name = document.getElementById("name")
let units = document.getElementById("units")
let price = document.getElementById("price")
let currency = document.getElementById("currency")
let fx_rate = document.getElementById("fx_rate")

asset_type.onchange = function() {
	if (asset_type.value == "cash") {
		symbol.hidden = true;
		name.hidden = true;
		units.placeholder = "Amount";
		price.placeholder = "FX Rate";

	} else if (asset_type.value == "real_estate") {
		symbol.hidden = true;
		name.hidden = false;
		units.hidden = true;
		price.placeholder="Price";
	} else if (asset_type.value == "gold") {
		symbol.hidden = false;
		symbol.placeholder = "Unit type(g, oz, paper)"
		name.hidden = true;
		units.hidden = false;
		price.placeholder = "Price"
		units.placeholder = "Units"

	} else if (asset_type.value == "stocks") {
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
	} else {
		fx_rate.hidden = true;
	}
}