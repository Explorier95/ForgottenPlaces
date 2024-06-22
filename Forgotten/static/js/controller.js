/*
* js file
* Fabian Tappendorf & Alissa Baumeister
*
* */

document.addEventListener('DOMContentLoaded', function() {
    mapboxgl.accessToken = 'pk.eyJ1IjoiYWxpc3NhamIiLCJhIjoiY2x4bXpqYW5tMGRobTJpczY1ZmNzaTFlbSJ9.cGqpPHYr4ezHEYYkKxtAeA';
    var map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v11',
        // style: 'mapbox://styles/mapbox/satellite-streets-v10' satellite view
        center: [13.40, 52.52], //Longitude & Latitude
        zoom: 6,
    });

    const layerList = document.getElementById('menu');
    const inputs = layerList.getElementsByTagName('input');

    for (const input of inputs) {
        input.onclick = (layer) => {
            const layerId = layer.target.id;
            map.setStyle('mapbox://styles/mapbox/' + layerId);
        };
    }
});


var places = document.querySelector('.place-item');
//function that sets a marker on the map for a specific coordinate (longitude/latitude)
//Array.prototype.forEach.call(places, (pl) => {
places.forEach(function(pl) {
    var name = pl.getAttribute('name');
    var longitude = parseFloat(pl.getAttribute('lon'));
    var latitude = parseFloat(pl.getAttribute('lat'));

    var marker = new mapboxgl.Marker()
        .setLngLat([longitude, latitude])
        .setPopup(new mapboxgl.Popup().setText(name)).addTo(map);
    });



