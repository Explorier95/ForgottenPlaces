

var map;
var markers = [];

// mapboxgl item initializing after dom loading
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM geladen");

    //load the mapbox api token
    fetch('/api/mapbox-token/')
        .then(response => response.json())
        .then(config => {
            mapboxgl.accessToken = config.token;
            initializeMap(); // Karte initialisieren
        })
        .catch(error => console.log(error));

        // initialize the map
        function initializeMap() {
        var map = new mapboxgl.Map({
            container: 'map',
            style: 'mapbox://styles/mapbox/streets-v11',
            center: [13.40, 52.52],
            zoom: 6
        });

        // Change from street to satellite view
        const layerList = document.getElementById('menu');
        if (layerList) {
            const inputs = layerList.getElementsByTagName('input');
            for (const input of inputs) {
                input.onclick = (layer) => {
                    const layerId = layer.target.id;
                    map.setStyle('mapbox://styles/mapbox/' + layerId);
                };
            }
        }

        // Set Markers for the list-elements on the map based on the coordinates
        var places = document.querySelectorAll('.place-item');
        places.forEach(function (pl) {
            var id = pl.getAttribute('id');
            var name = pl.getAttribute('data-name');
            var longitude = parseFloat(pl.getAttribute('data-lon'));
            var latitude = parseFloat(pl.getAttribute('data-lat'));
            var placeId = pl.getAttribute('data-id');

            console.log('Marker hinzufügen für:', name, longitude, latitude);

            if (!isNaN(longitude) && !isNaN(latitude)) {
                var marker = new mapboxgl.Marker()
                    .setLngLat([longitude, latitude])
                    .setPopup(new mapboxgl.Popup().setText(name))
                    .addTo(map);

                var clickCount = 0;
                //clicking the marker
                marker.getElement().addEventListener('click', function () {
                    console.log("Marker geklickt: ", marker);

                    clickCount++;

                    if (clickCount === 2) {
                        localStorage.setItem('scrollToPlaceId', placeId);
                        console.log('hallo : scrollToPlaceId', placeId);
                        window.location.href = '/places/';
                        clickCount = 0;
                    }
                });
            }
        });

            // scroll to place on list
            var placeId = localStorage.getItem('scrollToPlaceId');
            if (placeId) {
                setTimeout(function () {
                    var element = document.getElementById(placeId);
                    if (element) {
                        element.scrollIntoView({behavior: 'smooth', block: 'end'});
                        localStorage.removeItem('scrollToPlaceId');
                    }
                }, 1000);
            }
        }

    // Event listener for the button to navigate to the map
    var flyButton = document.getElementById("flyButton");
    if (flyButton) {
        flyButton.addEventListener('click', function(event) {
            event.preventDefault();

            var lon = parseFloat(flyButton.getAttribute('data-lon'));
            var lat = parseFloat(flyButton.getAttribute('data-lat'));

            if (!isNaN(lon) && !isNaN(lat)) {
                map.flyTo({
                    center: [lon, lat],
                    zoom: 12,
                    essential: true
                });
            }
        });
    }
});





