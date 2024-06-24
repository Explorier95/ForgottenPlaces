/*
* js file
* Fabian Tappendorf & Alissa Baumeister
*
* */

document.addEventListener('DOMContentLoaded', function() {
    console.log("JS geladen ");
    fetch('/static/js/token.json')
        .then(response => response.json())
        .then(config => {
            mapboxgl.accessToken = config.token;
            var map = new mapboxgl.Map({
                container: 'map',
                style: 'mapbox://styles/mapbox/streets-v11',
                // style: 'mapbox://styles/mapbox/satellite-streets-v10' satellite view
                center: [13.40, 52.52], //Longitude & Latitude
                zoom: 6,
            });

            //change view from streetview to satelliteview
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


            var places = document.querySelectorAll('.place-item');
            //function that sets a marker on the map for a specific coordinate (longitude/latitude)
            //Array.prototype.forEach.call(places, (pl) => {
            if (places.length > 0) {
                places.forEach(function (pl) {
                    var name = pl.getAttribute('data-name');
                    var longitude = parseFloat(pl.getAttribute('data-lon'));
                    var latitude = parseFloat(pl.getAttribute('data-lat'));

                    console.log('Adding marker:', name, longitude, latitude);

                    if (!isNaN(longitude) && !isNaN(latitude)) {
                        var marker = new mapboxgl.Marker()
                            .setLngLat([longitude, latitude])
                            .setPopup(new mapboxgl.Popup().setText(name)).addTo(map);
                    }
                });
            } else {
                console.log("no place found :(");
            }
        })
        .catch(error => console.log(error));
        });


