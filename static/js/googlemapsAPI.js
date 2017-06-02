// Google Maps API

function initMap() {

    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 3,
        center: {lat: 39.8282, lng: -98.5795} // Center geopoint of U.S.
    });

    $.get("/gmaps_data/chief", function(results) {console.log(results);


    // Add some markers to the map.
    // Note: The code uses the JavaScript Array.prototype.map() method to
    // create an array of markers based on a given "locations" array.
    // The map() method here has nothing to do with the Google Maps API.
    var markers = results.map(function(location, i) {
      return new google.maps.Marker({
        position: {'lat': location.lat, 'lng': location.lng},
        label: location.title
      });
    });

    // Add a marker clusterer to manage the markers.
    var markerCluster = new MarkerClusterer(map, markers,
        {imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'});
    });
}

