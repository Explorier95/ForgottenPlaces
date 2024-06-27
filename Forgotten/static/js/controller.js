var map;
var markers = [];

// Inititalisieren der Mapbox - Map nach dem DOM laden
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM geladen");

    //Laden des mapbox api token
    fetch('/api/mapbox-token/')
        .then(response => response.json())
        .then(config => {
            mapboxgl.accessToken = config.token;
            initializeMap(); // Karte initialisieren
        })
        .catch(error => console.log(error));

        // Initialisiere die Karte
        function initializeMap() {
        var map = new mapboxgl.Map({
            container: 'map',
            style: 'mapbox://styles/mapbox/streets-v11',
            center: [13.40, 52.52],
            zoom: 6
        });

        // Lesen der Koordinaten aus der URL
        var urlParams = new URLSearchParams(window.location.search);
        var lon = parseFloat(urlParams.get('lon'));
        var lat = parseFloat(urlParams.get('lat'));

        // Zoom zur Position wenn Koordinaten in der Url mitgegeben wurden
        if (!isNaN(lon) && !isNaN(lat)) {
            map.flyTo({
                center: [lon, lat],
                zoom: 12,
                essential: true
            });
        }

        // Ansicht wechseln von Satellit zu Streetview
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

        /// Setzen von Markern für die Listenelemente auf der Karte basierend auf den Koordinaten
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
                // Erst nach doppeltem Klicken zurück zur List View
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

            // Zurück zur Liste
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
});





