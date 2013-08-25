var map;
var Latlng = new google.maps.LatLng(39.952092, -75.190271);
var myOptions = {
    zoom: 15,
    center: Latlng,
    mapTypeId: 'roadmap'
};
var marker = new google.maps.Marker({
    position: Latlng,
    title:"the University of Pennsylvania"
});
map = new google.maps.Map($('#map')[0], myOptions);
marker.setMap(map);

$(document).ready(function() {
  $("#submit_contact").click(function(event) {
    event.preventDefault();
    var datastring = $("#contact_form").serialize();
    $.ajax({
            type: "POST",
            url: "/contact/",
            data: datastring,
            success: function(data) {
              $('.form').html('Form has been submitted!');
            }
    });
  });
});

