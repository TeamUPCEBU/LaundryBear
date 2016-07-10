$(document).ready(function() {
	loadTable();
	calculateServiceFee();
	updateTotals();
});

function calculateServiceFee() {
	var total = 0;
	$("#table-body").children().each(function(index, element) {
		total += +$(element).data("price").valueOf();
	});
	var fee = total * serviceRate;
	$("#servicecharge").html(fee.toFixed(2));
}

function loadTable() {
	var selectedServices = document.cookie.replace(/(?:(?:^|.*;\s*)selectedServices\s*\=\s*([^;]*).*$)|^.*$/, "$1");

	if (selectedServices.length === 0) {
		selectedServices = [];
	} else {
		selectedServices = JSON.parse(selectedServices);
	}
	$.each(selectedServices, function(index, service) {
		insertRow(service);
	});
}

function updateTotals() {
	var total = 0;
	$("#table-body").children().each(function(index, element) {
		total += +$(element).data("price").valueOf();
	});
	$("#subtotal").html(total.toFixed(2));
	total += +$("#deliveryfee").html();
    total += +$("#servicecharge").html();
	$("#price_field").val(total.toFixed(2));
	$("#total").html(total.toFixed(2));
}

function insertRow(service) {
	var template = $("#row-template").html();
	var compiledTemplate = template.replace(/__servicename__/, service.name).replace(/__pieces__/g, service.pieces).replace(/__price__/g, service.price).replace(/__pk__/, service.pk);


	$("#table-body").append(compiledTemplate);
}

$("#confirm").on("click", function() {
	var data = collectData();
	$.post(transactionUrl, data, function(response) {
		// clear cookies
		var services = document.cookie.replace(/(?:(?:^|.*;\s*)selectedServices\s*\=\s*([^;]*).*$)|^.*$/, "$1");
		document.cookie = "selectedServices=;expires=Thu, 01 Jan 1970 00:00:01 GMT;path=/;";

		// show modal
		$("#sendModal").foundation("reveal", "open");
		setTimeout(function() {
			document.location.replace(response);
		}, 5000);
	});
	return false;
});

function collectData() {
	var csrf = $.cookie('csrftoken');
	var services = document.cookie.replace(/(?:(?:^|.*;\s*)selectedServices\s*\=\s*([^;]*).*$)|^.*$/, "$1");
	var delivery_date = $("input[name=\"delivery_date\"]").val();
	var building = $("#id_building").val();
	var street = $("#id_street").val();
	var barangay = $("#id_barangay").val();
	var city = $("#id_city").val();
	var province = $("#id_province").val();
	var price = $("#price_field").val();

	return {csrfmiddlewaretoken: csrf, selectedServices: services, delivery_date: delivery_date, building: building, street: street, barangay: barangay, city: city, province: province, price: price};
}
