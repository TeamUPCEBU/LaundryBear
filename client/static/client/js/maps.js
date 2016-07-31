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



function populateInfoWindow(name, location, id){
  var infoContent =
  "<div id='content'>"+
    "<h5 id='firstHeading' class = 'firstHeading'>"+ name+"</h5>"+
    "<div id='bodyContent'>"+
      "<p>" + location + "</p>"+
      "<a href='/order/"+ id + "' class='button'>Order</a>"+
    "</div>"+
  "</div>";

  var infoWindow = new google.maps.InfoWindow({
    content: infoContent,
    maxWidth : 200
  });
  return infoWindow;
}

function markLaundryLocation(geocoder, resultsMap) {
  var laundryMarker = {
    url: laundryIcon,
    size: new google.maps.Size(40, 50),
    origin: new google.maps.Point(0, 0),
    anchor: new google.maps.Point(0, 32)
  };

  for(var i = 0 ; i<parsedShopList.length ; i++){
    var match = $.when(geocodeThis(geocoder, parsedShopList[i].location), parsedShopList[i]);
    match.done(function (position, shop) {
        var infoWindow = populateInfoWindow(shop.name, shop.location, shop.id);
        var marker = new google.maps.Marker({
          map: resultsMap,
          position: position,
          icon: laundryMarker
        });
        marker.addListener('click',function(){
          infoWindow.open(resultsMap, marker);
        });

      });
  }
}


function geocodeThis(geocoder, address){
  var deferred = $.Deferred();
  geocoder.geocode({'address':address}, function(results, status) {
    if (status === google.maps.GeocoderStatus.OK) {
        var position = results[0].geometry.location;
        deferred.resolve(position);
    } else {
      var message = 'Geocode was not successful for the following reason: ' + status;
      alert(message);
      deferred.reject(message);
    }
  });
  return deferred.promise();
}


function marklocation(geocoder, map, coordinates){
    geocoder.geocode({'location': coordinates}, function(results, status) {
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
