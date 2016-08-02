$(document).ready(function() {
	$('.nothing-label').show();
	$('.request-button').hide();

	$('.service-choices').on('change', function(e){
		var service = e.target;
		var serviceModal = $('#serviceModal');
		console.log();
		serviceModal.find('h3').html($(service).find(":selected").html());
		serviceModal.find('#servicePrice').html("<i class='fa fa-fw fa-money'></i>").append("  Price: "+ $(service).find(":selected").data('price') + " per kilo.");
		serviceModal.find('#serviceDescription').html("<i class = 'fa fa-fw fa-list-alt'></i>").append("  Description: "+ $(service).find(":selected").data('description'));
		$('#serviceModal').openModal();
		return false;
	})

	$('.add-to-basket').click(function(e){
		e.preventDefault();

		$('#serviceModal').closeModal();

		var serviceOrder = $('.service-orders');

		var numberOfClothes = parseInt($('.num-clothes').val());

		var chosenService = $('.service-choices').find(":selected");

		var pricepk = chosenService.val();
		var pieces = parseInt($('.num-clothes').val());

		var estimatedPrice = ((parseInt($('.num-clothes').val()) * parseInt($('.service-choices').find(":selected").data('price')))/7).toFixed(2);
		// this part adds to basket
		if ($('.num-clothes').val() == 0){
			Materialize.toast('Invalid Transaction. Choose Service Again.', 2000, '', function(){
				document.location.replace(response);
			});
			return false;
		}
		else {
			$('.request-button').show();
			var newBasketItem = $("<li>"+
			"<div class='collapsible-header'>"+
				$('.service-choices').find(":selected").html()+
			"</div> "+
			"<div class = 'collapsible-body' style='padding: 15px 15px 15px 15px'>"+
				"<div class='row'>"+
					"<div class='col s6 center num'><span><i class='fa fa-fw fa-hashtag'></i>&nbsp;No. of Items: "+ $('.num-clothes').val() +"</span></div>"+
					"<div class='col s6 center ep'><span><i class='fa fa-fw fa-money'></i>&nbsp;Estimated Price: "+ estimatedPrice +"</span></div>"+
				"</div>"+
				"<div class='row center' style='margin-top:10px'>"+
					"<a class='btn delete-service red waves-effect waves-light' href='#'>Delete</a>"+
				"</div>"+
			"</div>"+
			"</li>");
			// final steps
			//"<div hidden class='basketitem' data-pk="+ pricepk + " data-pieces="+ pieces  +"></div>" +
			newBasketItem.attr('data-num',$('.num-clothes').val())
									 .attr('data-estimate',estimatedPrice)
									 .attr('data-pk', pricepk);
			serviceOrder.append(newBasketItem);
			serviceOrder.collapsible({accordion:false});
			$('.num-clothes').val('0');
			$('.nothing-label').hide();
		}
	})

	$('.num-clothes').on('focus',function(){
		$(this).val('');
	})

	$('.service-orders').on('click', '.delete-service',function(e){
		e.preventDefault();
		$(e.target).closest('li').fadeOut("slow",function(){
			$(this).remove();
			if ($(this).closest('ul').length== 0){
					$('.request-button').hide();
			} ;
		});

	})


	$('.request-button').on('click',function(e){
		var summaryTable = $('.summary-table').find('tbody');
		var subTotal = 0.0;
		var total = 0.0;
		summaryTable.html("");
		$('.service-orders li').each(function(index,element){
			$("<tr><td>"+$(element).find('.collapsible-header').text()+"</td><td>"+$(element).data('num')+"</td><td>"+$(element).data('estimate')+"</td></tr>")
			.appendTo(summaryTable);
			subTotal += $(element).data('estimate');
		});
		$('.subtotal-value').text("PHP "+ subTotal);

		total = total + subTotal;
		total = total + (total * $('#serviceCharge').data('service'));
		total = total + parseFloat($('#deliverFee').data('deliver'), 10);
		total = parseFloat(total).toFixed(2);
		$('#total-payment').text("Total: PHP ");
		$('#total_value').text(total);
		})


		function collectData() {
			var csrf = document.cookie.replace(/(?:(?:^|.*;\s*)selectedServices\s*\=\s*([^;]*).*$)|^.*$/, "$1");
			var services = [];

			$('.service-orders li').each(function(index,element){
				var thePieces = $(this).data('num');
				var theEstimate = $(this).data('estimate');
				var thePk = $(this).data('pk');
				var priceData = {pk:thePk, pieces:thePieces};
				services.push(priceData);
			});

			services = JSON.stringify(services);
			//services = services.replace(/\\/g, "");

			var delivery_date = $("input[name=\"delivery_date\"]").val();
			var building = $("#id_building").val();
			var street = $("#id_street").val();
			var barangay = $("#id_barangay").val();
			var city = $("#id_city").val();
			var province = $("#id_province").val();
			var price = $('#total_value').text();
			var fees = $('#serviceCharge').data('pk');
			return {csrfmiddlewaretoken: csrf, selectedServices: services, delivery_date: delivery_date, building: building, street: street, barangay: barangay, city: city, province: province, price: price, fee: fees};
		}



	$("#confirm").on("click", function() {

		var data = collectData();
		$.post(transactionUrl, data, function(response) {
			Materialize.toast('Request sent!', 2000, '', function(){
				document.location.replace(response);
			});
		});
		return false;
		});


	$('#review').on('click', function(e){
		e.preventDefault();
		$('#comment-modal').openModal();
	});

	$('#close-comment-modal').on('click', function(e){
		e.preventDefault();
	});

});
