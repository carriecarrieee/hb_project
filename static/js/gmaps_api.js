// Google Maps API


function initMap() {

    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 4,
        center: {lat: 37.0902, lng: -95.7129} // Center geopoint of U.S.
    });

    $(document).ready(function() {
    if (window.location.pathname == '/dashboard') {
        $.get("/gmaps_data", { search_input: $("#search_term").text() }, 
            function(results) {console.log(results);

            // Add markers to the map.
            // "icon" is an object within Google Maps, like a dictionary
            var icon = {
                url: "/static/js/markerClusterer/job.png", // url
                scaledSize: new google.maps.Size(30, 30), // scaled size
            };


            var markers = results.map(function(location, i) {
                return new google.maps.Marker({
                    position: {'lat': location.lat, 'lng': location.lng},
                    title: location.emp,
                    map: map,
                    icon: icon
                });
            });

             // Add a marker clusterer to manage the markers.
            var markerCluster = new MarkerClusterer(map, markers,
                {imagePath: '/static/js/markerClusterer/m'});           

            map.setCenter(markers[markers.length]);
            });
        }
        
    });
}

