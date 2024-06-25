/*
* js file
* Fabian Tappendorf & Alissa Baumeister
*
* */
var map;
var markers = [];

// mapboxgl item initializing after dom loading
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM geladen");

    //load token from the json
    fetch('/static/js/token.json')
        .then(response => response.json())
        .then(config => {
            mapboxgl.accessToken = config.token;
            initializeMap();
        })
        .catch(error => console.log(error));

// function to inititalize the whole map
function initializeMap() {
    map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v11',
        center: [13.40, 52.52],
        zoom: 6,
    });

    // change view from satellite to streetview
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

    // put markers for places on the map via coordinates
    var places = document.querySelectorAll('.place-item');
    if (places.length > 0) {
        places.forEach(function (pl) {
            var name = pl.getAttribute('data-name');
            var longitude = parseFloat(pl.getAttribute('data-lon'));
            var latitude = parseFloat(pl.getAttribute('data-lat'));
            var placeId = pl.getAttribute('id');

            console.log('Marker hinzufügen für:', name, longitude, latitude);

            if (!isNaN(longitude) && !isNaN(latitude)) {
                var marker = new mapboxgl.Marker()
                    .setLngLat([longitude, latitude])
                    .setPopup(new mapboxgl.Popup().setText(name))
                    .addTo(map);

                //add to array
                markers.push({marker: marker, placeId: placeId});

                marker.getElement().addEventListener('click', function () {
                    console.log("marker clicked: ", marker);
                    localStorage.setItem('scrollToPlaceId', placeId);
                    window.location.href = '/places/';

                });
            }
        });

        function showToast(name) {
            // toast dialoge fürs debuugging
            alert('Marker geklickt: ' + name);
        }

        var placeId = localStorage.getItem('scrollToPlaceId');
        if (placeId) {
            setTimeout(function () {
                var element = document.getElementById(placeId);
                if (element) {
                    element.scrollIntoView({behavior: 'smooth', block: 'end'});
                    // Clear the stored place ID after scrolling
                    localStorage.removeItem('scrollToPlaceId');
                }
            }, 1000);
        }


    var zoomButtons = document.querySelectorAll('.flyButton');
    zoomButtons.forEach(function (button) {
    // Hier kannst du Aktionen für jedes 'button' Element durchführen
    button.addEventListener('click', function(event) {
        // Beispiel: Klick-Ereignis hinzufügen
        event.preventDefault();
        console.log('Button geklickt:', button.textContent);
    });

    var lon = parseFloat(button.getAttribute('data-lon'));
    var lat = parseFloat(button.getAttribute('data-lat'));
    console.log('Name:', name, 'Longitude:', lon, 'Latitude:', lat);
                if (!isNaN(lon) && !isNaN(lat)) {
                    map.flyTo({
                        center: [lon, lat],
                        zoom: 25,
                        essential: true
                    });
                }
            });

    }
}
});


//TODO vielleicht hier mit json arbeiten oder daten nur in sitzung speichern oder so ?



