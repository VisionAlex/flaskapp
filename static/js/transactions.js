const asset_type = document.querySelector("#asset_type");
const symbol = document.querySelector("#symbol");
const name = document.querySelector("#name");
const units = document.querySelector("#units");
const price = document.querySelector("#price");
const currency = document.querySelector("#currency");
const fx_rate = document.querySelector("#fx_rate");
const fx_help = document.querySelector("#fx_help");

asset_type.addEventListener('change', result)

function result(){

	switch (asset_type.value) {
		case "Cash":
			symbol.hidden = true;
			name.hidden = true;
			units.placeholder = "Amount";
			price.placeholder = "FX Rate";
			break;
		case "Real Estate":
			symbol.hidden = false;
			name.hidden = false;
			units.hidden = true;
			symbol.placeholder = "ex: ESTATE1";
			price.placeholder ="Price";
			break;
		case "Gold":
			symbol.hidden = false;
			symbol.placeholder = "Unit type(g, oz, paper)";
			name.hidden = true;
			units.hidden = false;
			price.placeholder = "Price";
			units.placeholder = "Units";
			break;
		case "Stocks":
			symbol.hidden = false;
			symbol.placeholder = "Symbol";
			symbol.required = true;
			name.hidden = false;
			units.hidden = false;
			units.placeholder = "Shares";
			price.placeholder = "Price";
			break;
		default:
			symbol.hidden = false;
			price.placeholder = "Price";
			units.hidden = false;
			name.hidden = false;
			symbol.required = false;
			symbol.placeholder = "";


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