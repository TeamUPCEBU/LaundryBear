$(document).ready(function(){
  $(".button-collapse").sideNav();
  $('.collapsible').collapsible({
    accordion : false // A setting that changes the collapsible behavior to expandable instead of the default accordion style
  });

  $('select').material_select();
  $('.modal-trigger').leanModal();
})
