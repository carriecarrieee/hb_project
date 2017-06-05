// Google Maps API


function initMap() {

    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 3,
        center: {lat: 37.0902, lng: -95.7129} // Center geopoint of U.S.
    });

    $(document).ready(function() {
    if (window.location.pathname == '/dashboard') {
        $.get("/gmaps_data", { search_term: $("#search_term").val() }, 
            function(results) {console.log(results);

            // Add markers to the map.
            var markers = results.map(function(location, i) {
                return new google.maps.Marker({
                    position: {'lat': location.lat, 'lng': location.lng},
                    title: "location.title",
                    map: map
                });
            });

             // Add a marker clusterer to manage the markers.
            var markerCluster = new MarkerClusterer(map, markers,
                {imagePath: '/static/js/markerClusterer/m'});           

            map.setCenter(markers[markers.length - 1].getPosition());
            });

    }

});



}

