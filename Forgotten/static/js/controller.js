/*
* js file
* Fabian Tappendorf & Alissa Baumeister
*
* */
var map;

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
});

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

            console.log('Marker hinzufügen für:', name, longitude, latitude);

            if (!isNaN(longitude) && !isNaN(latitude)) {
                var marker = new mapboxgl.Marker()
                    .setLngLat([longitude, latitude])
                    .setPopup(new mapboxgl.Popup().setText(name))
                    .addTo(map);
            }
        });
    } else {
        console.log("Keine Orte gefunden :(");
    }
}

//show element on map via zoom in when element is clicked in list
function zoomToMarker(longitude, latitude) {
    document.getElementById("flyButton").addEventListener('click', () => {
        console.log("fly me to the moon");
        map.flyTo({
            center: [longitude, latitude],
            zoom: 25,
            essential: true
        });
    });
}
