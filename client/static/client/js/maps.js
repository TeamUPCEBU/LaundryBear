
function displayMap() {
      navigator.geolocation.getCurrentPosition(function(position) {
          var coordinates = new google.maps.LatLng(position.coords.latitude,
              position.coords.longitude);
          var geocoder = new google.maps.Geocoder;
          var mapDiv = document.getElementById('mapsDiv');

          var mapOptions = {
            center: coordinates,
            zoom: 17,
            scrollwheel:false,
            mapTypeId: google.maps.MapTypeId.TERRAIN,
            streetViewControl: false,
            rotateControl: false,
            mapTypeControl: false
          }
          var map = new google.maps.Map(mapDiv, mapOptions);

          google.maps.event.addListenerOnce(map, 'idle', function(){
            marklocation(geocoder, map, coordinates);
          });
      });
}

function setLocationFromAddress(geocoder){

}


function marklocation(geocoder, map, coordinates){
    geocoder.geocode({'location': coordinates}, function(results, status) {
        console.log('twwwooo');
        if (status === google.maps.GeocoderStatus.OK) {
            if (results[0]) {
              var marker = new google.maps.Marker({
                  position: coordinates,
                  map: map,
                  title: results[0].formatted_address
              });
            } else {
                alert('No results found');
            }
        }
        else {
          alert('Geocoder failed due to: ' + status);
        }
    });
}
