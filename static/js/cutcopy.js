$(document).ready(function () {
  //Disable cut copy paste
  $('body').bind('cut copy paste inspect', function (e) {
    e.preventDefault();
  });

  //Disable mouse right click
  $("body").on("contextmenu", function (e) {
    return false;
  });

});
