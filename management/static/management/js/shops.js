$(".activate-shop-button").on("click", function(){
    var status = 2;
    var doneUrl = $(this).data("done-url");
    var token = document.cookie.replace(/(?:(?:^|.*;\s*)csrftoken\s*\=\s*([^;]*).*$)|^.*$/, "$1");
    var that = $(this);
    console.log(doneUrl);
    $.post(doneUrl, {status: status, csrfmiddlewaretoken: token}, function(response) {
        var revealId = that.data("reveal-id");
        $("#" + revealId).foundation("reveal", "open");
        setTimeout(function() {
            $("#" + revealId).foundation("reveal", "close");
        }, 500);
        that.closest("tr").remove();
    });
});


$(".reload-credits").on("click", function(){
    var deleteLoadRequestUrl = $(this).data('delete-load-request-url');
    var doneUrl = $(this).data("done-url");
    var token = document.cookie.replace(/(?:(?:^|.*;\s*)csrftoken\s*\=\s*([^;]*).*$)|^.*$/, "$1");
    var that = $(this);
    var credits = parseInt(that.data('credits')) + parseInt(that.data('amount'));

    $.when(
        $.post(doneUrl, {csrfmiddlewaretoken: token, credits: credits}, function(response) {})
    ).done(function(){

        $.post(deleteLoadRequestUrl,{csrfmiddlewaretoken: token},function(response){
            that.closest("tr").remove();
            var revealId = that.data("reveal-id");
            $("#" + revealId).foundation("reveal", "open");
            setTimeout(function() {
                $("#" + revealId).foundation("reveal", "close");
            }, 500);
        });

    });
});


