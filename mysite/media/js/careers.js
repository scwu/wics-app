$(document).ready(function() {
  var opps = ["intern", "full-time", "scholarship", "conference"]
  $(".opportunity").hide();
  $("div#intern").show();
  $(".important").click(function(event) {
    var el_id = $(this).attr('id');
    var id_selector = "div#" + el_id;
    for (var i = 0; i < opps.length; i++) {
      if (opps[i] != el_id) {
        var id_selector2 = "div#" + opps[i];
        $(id_selector2).hide();
        $('.important').css({'background-color' : '#808080'});
      }
    }
    $(id_selector).show();
    $(this).css({'background-color': '#66CCFF'});
   });
});
