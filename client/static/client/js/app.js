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



$('#logout_submit').click(function(){$('#logout_form').submit();});


$(document).ready(function() {
    $("#buttonForModal").click(function() {
      $("#myModal").reveal();
    });
  });

$(".reveal-modal-button").click(function() {
	var modalId = $(this).data("reveal-id");
	$("#" + modalId + " input").val(0);
});


$(document).foundation({
    tab: {
      callback : function (tab) {
        console.log(tab);
      }
    }
});

$('#myTabs').on('toggled', function (event, tab) {
    console.log(tab);
});
