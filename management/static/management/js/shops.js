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
        }, 1000);
        that.closest("tr").remove();
    });
});
