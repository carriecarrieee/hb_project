// Google Maps API
var markers;

function initMap() {

    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 3,
        center: {lat: 39.8282, lng: -98.5795} // Center geopoint of U.S.
    });

    $(document).ready(function() {
    if (window.location.pathname == '/dashboard') {
        $.get("/gmaps_data", { skill: $("#search_term").val() }, function(results) {
            console.log(results);

        markers = results.map(function(location, i) {
            return new google.maps.Marker({
            position: {'lat': location.lat, 'lng': location.lng},
            label: location.title,
            map: map
            });
        });
        
        map.setCenter(markers[markers.length - 1].getPosition());

        });
    }

});

    // Add markers to the map.
    // Add a marker clusterer to manage the markers.
    var markerCluster = new MarkerClusterer(map, markers,
        {imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'});
}

