/*
* js file
* Fabian Tappendorf & Alissa Baumeister
*
* */
document.addEventListener("DOMContentLoaded", function() {
mapboxgl.accessToken = 'pk.eyJ1IjoiYWxpc3NhamIiLCJhIjoiY2x4bXpqYW5tMGRobTJpczY1ZmNzaTFlbSJ9.cGqpPHYr4ezHEYYkKxtAeA';
    var map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v11',
        // style: 'mapbox://styles/mapbox/satellite-streets-v10' satellite view
        center: [13.40, 52.52], //Longitude & Latitude
        zoom: 7
    });
});