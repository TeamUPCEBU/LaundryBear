$('.raty-rating').raty({
    half: true,
    readOnly: true,
    score: function() {
        return $(this).attr('data-value');
    }
});


$('.raty-click').click(function() {

        var _id = $(this).attr('id');
        $(this).parent('#paws').replaceWith(
            '<div class="raty">' + '</div>'+
            '<input type="hidden" id="input_id" name="" value=""/>'+
            '<input type="hidden" id="input_num" name="" value=""/>'+
            '<input type="submit" class="btn light-blue waves-effect waves-light" value="Submit"/>'
        );

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
