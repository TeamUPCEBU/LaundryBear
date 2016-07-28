function displayMap() {
  navigator.geolocation.getCurrentPosition(function(position) {
    var coordinates = new google.maps.LatLng(position.coords.latitude,
        position.coords.longitude);
    var geocoder = new google.maps.Geocoder;
    var mapDiv = document.getElementById('mapsDiv');

    var mapOptions = {
      center: coordinates,
      zoom: 15,
      scrollwheel:false,
      mapTypeId: google.maps.MapTypeId.TERRAIN,
      streetViewControl: false,
      rotateControl: false,
      mapTypeControl: false
    }
    var map = new google.maps.Map(mapDiv, mapOptions);

    google.maps.event.addListenerOnce(map, 'idle', function(){
      marklocation(geocoder, map, coordinates);
      markLaundryLocation(geocoder,map);
    });
  });
}

function markLaundryLocation(geocoder, resultsMap) {
  for(var i = 0 ; i<parsedShopList.length ; i++){
    var shopL = parsedShopList[i];
    geocoder.geocode({'address':parsedShopList[i].location}, function(results, status) {
      if (status === google.maps.GeocoderStatus.OK) {
        console.log(laundryIcon);
        var laundryMarker = {
          url: laundryIcon,
          // This marker is 20 pixels wide by 32 pixels high.
          size: new google.maps.Size(40, 50),
          // The origin for this image is (0, 0).
          origin: new google.maps.Point(0, 0),
          // The anchor for this image is the base of the flagpole at (0, 32).
          anchor: new google.maps.Point(0, 32)
        };
        var marker = new google.maps.Marker({
          map: resultsMap,
          position: results[0].geometry.location,
          title: shopL.name + "\n" + shopL.location,
          icon: laundryMarker
        });
      } else {
        alert('Geocode was not successful for the following reason: ' + status);
      }
    });
  }
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
