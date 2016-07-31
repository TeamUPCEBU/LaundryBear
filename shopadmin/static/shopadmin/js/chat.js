$('div #chat-trigger').click(function(e){
  e.stopPropagation();
  e.preventDefault();
  $('#chatfield').toggle();
});

$('#send-message').click(function(e){
  e.stopPropagation();
  e.preventDefault();


  var message = $('#message-field').val();
  if ( message || message.replace(/\s/g, '').length ){

    $('#message-field').val('');
    $('#chatbox').append(
        "<div class='alert-box succeess round' align='right'>"+
        message
        + "</div>"
    );

    $('#chatbox').append(
        "<div class='alert-box secondary round'>"+
        " hey mang "
        + "</div>"
    );


    $('#chatbox').scrollTop($('#chatbox')[0].scrollHeight);
  }
});
