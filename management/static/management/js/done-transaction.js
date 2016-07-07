$(".done-button").on("click", function(){
    var status = 3;
    var doneUrl = $(this).data("done-url");
    var token = document.cookie.replace(/(?:(?:^|.*;\s*)csrftoken\s*\=\s*([^;]*).*$)|^.*$/, "$1");
    var that = $(this);
    $.post(doneUrl, {status: status, csrfmiddlewaretoken: token}, function() {
        var revealId = that.data("reveal-id");
        $("#" + revealId).foundation("reveal", "open");
        setTimeout(function() {
            $("#" + revealId).foundation("reveal", "close");
        }, 1000);
        that.closest("tr").remove();
    });
});