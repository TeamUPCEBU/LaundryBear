$(document).ready(function() {
	$('.nothing-label').show();

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
		console.log($('.service-choices').find(":selected").html());
		var serviceOrder = $('.service-orders');
		var estimatedPrice = ((parseInt($('.num-clothes').val()) * parseInt($('.service-choices').find(":selected").data('price')))/7).toFixed(2);
		// this part adds to basket
		if ($('.num-clothes').val() == 0){

			return false;
		}
		else {
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
			newBasketItem.attr('data-num',$('.num-clothes').val()).attr('data-estimate',estimatedPrice);
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
		});
	})

	$('.request-button').on('click',function(e){
		var summaryTable = $('.summary-table').find('tbody');
		var subTotal = 0;
		var total = 0;
		summaryTable.html("");
		$('.service-orders li').each(function(index,element){
			$("<tr><td>"+$(element).find('.collapsible-header').text()+"</td><td>"+$(element).data('num')+"</td><td>"+$(element).data('estimate')+"</td></tr>")
			.appendTo(summaryTable);
			subTotal += $(element).data('estimate');
		});
		$('.subtotal-value').text("PHP "+ subTotal);
		total = (subTotal + parseFloat($('#serviceCharge').data('service')) + parseFloat($('#deliverFee').data('deliver'))).toFixed(2);
		$('.total-payment').html("Total: PHP "+total);
	})
});
