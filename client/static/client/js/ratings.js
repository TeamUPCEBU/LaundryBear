$('.raty-rating').raty({
    half: true,
    readOnly: true,
    score: function() {
        return $(this).attr('data-value');
    }
});


$('.raty-click').click(function() {

        var _id = $(this).attr('id');
        $(this).parent().find('.rate').show();
        $(this).hide();

        $('div.raty').raty({
            id: _id,
            click: function(score, evt) {
                $('#input_id').attr('name','id');
                $('#input_id').attr('value',_id);
                $('#input_num').attr('name','score');
                $('#input_num').attr('value',score);
            }
        });
    }
);


$('.raty').click(function(){
  $(this).parent().find('.submit-feedback').removeClass('disabled');
});
