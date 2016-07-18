$(document).foundation();

$(window).bind("load", function () {
   var footer = $("#footer");
   var pos = footer.position();
   var height = $(window).height();
   height = height - pos.top;
   height = height - footer.height();
   if (height > 0) {
       footer.css({
           'margin-top': height + 'px'
       });
   }
});

$(document).foundation({
    reveal : {
        multiple_opened:true
    }
});

$('#drop1 option').click(function(){
  var value = $(this).val();
  $('#selected').html(value);
});

$("dl.sub-nav dd").click(function(){
  $("dl.sub-nav dd.active").removeClass("active");
  $(this).addClass("active");
  $("#search").prop("name", $(this).children().html().toLowerCase());
  return false;
});

$("#open-time, #close-time").on("change", function() {
	var openTime = $("#open-time").val();
	var closeTime = $("#close-time").val();

	if (openTime === "null" || closeTime === "null" || openTime === null || closeTime === null) {
		$("#id_hours_open").val('');
	}
  else{
	var timeString = openTime + ' - ' + closeTime;

	$("#id_hours_open").val(timeString);
}
});

$("#days-container input").on("change", function() {
	var checked = [];
	$("#days-container input").each(function(index, element) {
		var $element = $(element);
		if ($element.prop("checked")) {
			checked.push($element.next().html());
		}
	});
	var dayString = checked.join(', ');
	$("#id_days_open").val(dayString);
});

$('#logout_submit').click(function(){$('#logout_form').submit();});

// $("#new-service-modal-close-reveal").click(function(){$('form')[0].reset();});

 $("#new-service-modal-close-reveal").click(function(){
 	$("#sname").val("");
 	$("#desc").val("");
 });
