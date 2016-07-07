$(document).ready(function() {
	loadServices();
});

function loadServices() {
	// load from cookies
	var services = document.cookie.replace(/(?:(?:^|.*;\s*)selectedServices\s*\=\s*([^;]*).*$)|^.*$/, "$1");
	if (services.length === 0) {
		return false;
	}
	services = JSON.parse(services);
	$.each(services, function(index, service) {
		insertRow(service);
	});
	updateTotals();
}

$("#drop1 li").click(function() {
	if ($(this).prop("disabled")) {
		return false;
	}
});

$(".add-to-basket").on("click", addToBasket);


function addToBasket() {
	var pieces = $(this).siblings("input").val();
	pieces = parseFloat(pieces).toFixed(0);
	if (pieces.length === 0 || pieces == 0) {
		return false;
	}

	var servicename = $(this).data("servicename");
	var pk = $(this).data("pk")
	var pricePerKg = $(this).data("price-per-kilo");
	var price = pieces * pricePerKg / 7;
	price = parseFloat(price).toFixed(2);
	var service = {name: servicename, price: price, pieces: pieces, pk: pk, pricePerKg: pricePerKg};
	insertRow(service);

	$(this).siblings("input").val("");
	$(this).parent().foundation("reveal", "close");

	// save into cookie
	// document.cookie.replace(/(?:(?:^|.*;\s*)test2\s*\=\s*([^;]*).*$)|^.*$/, "$1");
	var selectedServices = document.cookie.replace(/(?:(?:^|.*;\s*)selectedServices\s*\=\s*([^;]*).*$)|^.*$/, "$1");
	if (selectedServices.length === 0) {
		selectedServices = [];
	} else {
		selectedServices = JSON.parse(selectedServices);
	}
	selectedServices.push({name: servicename, pk: pk, pricePerKg: pricePerKg, price: price, pieces: pieces, pricePerKg: pricePerKg});
	document.cookie = "selectedServices=" + JSON.stringify(selectedServices) + ";path=/;domain=;";

	updateTotals();
}

function insertRow(service) {
	var template = $("#row-template").html();
	var compiledTemplate = template.replace(/__servicename__/, service.name).replace(/__pieces__/g, service.pieces).replace(/__price__/g, service.price).replace(/__pk__/, service.pk).replace(/__pricePerKg__/, service.pricePerKg);

	// disable
	$("#drop1 li[value=\"" + service.pk + "\"]").prop("disabled", true);
	$("#drop1 li[value=\"" + service.pk + "\"] a").css("cursor", "not-allowed");

	$("#table-body").append(compiledTemplate);
}

function updateTotals() {
	var total = 0;
	$("#table-body").children().each(function(index, element) {
		total += +$(element).data("price").valueOf();
	});
	$("#total-price").html(total.toFixed(2));
}

$("#table-body").on("click", ".alert", function(e) {
	var selectedServices = document.cookie.replace(/(?:(?:^|.*;\s*)selectedServices\s*\=\s*([^;]*).*$)|^.*$/, "$1");
	selectedServices = JSON.parse(selectedServices);
	var index = $("#table-body .alert").index(this);
	selectedServices.splice(index, 1);
	document.cookie = "selectedServices=" + JSON.stringify(selectedServices) + ";path=/;domain=;";
	$(e.target).closest("tr").remove();
	updateTotals();
	return false;
});


$("#table-body").on("click", ".info", function(e) {
	var revealId = $(e.target).data("reveal-id");
	var modal = $("#" + revealId);
	modal.foundation("reveal", "open");
	var items = $(e.target).data("pieces");
	modal.find("input").val(+items);
	var selectedServices = document.cookie.replace(/(?:(?:^|.*;\s*)selectedServices\s*\=\s*([^;]*).*$)|^.*$/, "$1");
	selectedServices = JSON.parse(selectedServices);
	var index = $("#table-body .info").index(this);
	var removed = selectedServices.splice(index, 1)[0];
	var pricePerKg = $(this).data("price-per-kg");

	modal.find(".add-to-basket").unbind();
	modal.find(".add-to-basket").one("click", function() {
		var items = $(this).parent().find("input").val();
		$(this).on("click", addToBasket);
		if (items.length === 0 || items == 0) {
			return false;
		}
		console.log(items);
		$(e.target).closest("tr").remove();
		document.cookie = "selectedServices=" + JSON.stringify(selectedServices) + ";path=/;domain=;";
		// add edited
		$(this).data("price-per-kilo", pricePerKg);
		$(this).trigger("click");
		return false;
	});
	return false;
});

$(".button.left").click(function() {
	// clear cookies
	var services = document.cookie.replace(/(?:(?:^|.*;\s*)selectedServices\s*\=\s*([^;]*).*$)|^.*$/, "$1");
	document.cookie = "selectedServices=;expires=Thu, 01 Jan 1970 00:00:01 GMT;path=/;";
});
