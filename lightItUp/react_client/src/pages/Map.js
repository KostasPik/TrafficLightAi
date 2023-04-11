import React, { useEffect } from 'react'
import './Map.css'
function Map() {



    useEffect(() => {
        var duplicateScript = document.getElementById("mapScript");
        if (duplicateScript) return;
        const inlineScript = document.createElement('script');
        inlineScript.setAttribute("id", "mapScript");
        inlineScript.innerHTML = `mapboxgl.accessToken = 'pk.eyJ1Ijoiam1sYWJzIiwiYSI6Imlnc1pXbncifQ.1U4VwxWkGS_Y3TpZ6-sf4A'

        const athensLat = 37.983810;
        const athensLong = 23.727539;
        
        const map = new mapboxgl.Map({
            container: 'map', // container ID
            projection:'equirectangular',
            // Choose from Mapbox's core styles, or make your own style with Mapbox Studio
            style: 'mapbox://styles/mapbox/streets-v12', // style URL
            center: [athensLong, athensLat], // starting position [lng, lat]
            zoom: 13 // starting zoom
        });
        map.addControl(new mapboxgl.NavigationControl());

        
        const preloaderDiv = document.getElementById('preloader');
        const mapDiv = document.getElementById('map');
        
        const SERVER_URL = 'lightitup-1-e1507095.deta.app'
        
        
            // Mapbox expressions to filter based on property 'traffic' : 0/1/2
            const traffic0 = ['==', ['get', 'traffic'], 0] 
            const traffic1 = ['==', ['get', 'traffic'], 1]
            const traffic2 = ['==', ['get', 'traffic'], 2]
        
            map.on('load', async () => {
                const response = await fetch("https://"+SERVER_URL+"/get-traffic/");
                const trafficDataJson = await response.json();
        
               await map.addSource('trafficLights', {
                    type: 'geojson',
                    // Point to GeoJSON data. This example visualizes all M1.0+ earthquakes
                    // from 12/22/15 to 1/21/16 as logged by USGS' Earthquake hazards program.
                    data: trafficDataJson,
                    cluster: true,
                    clusterMaxZoom: 14, // Max zoom to cluster points on
                    clusterRadius: 50, // Radius of each cluster when clustering points (defaults to 50)
                    clusterProperties: {
                        'traffic0': ['==', ['case',traffic0,1, 0]],
                        'traffic1': ['==', ['case',traffic1,1, 0]],
                        'traffic2': ['==', ['case',traffic2,1, 0]],
                    }
                });
        
                await map.addLayer({
                    id: 'clusters',
                    type: 'circle',
                    source: 'trafficLights',
                    filter: ['has', 'point_count'],
                    paint: {
                        // Use step expressions (https://docs.mapbox.com/mapbox-gl-js/style-spec/#expressions-step)
                        // with three steps to implement three types of circles:
                        //   * Blue, 20px circles when point count is less than 100
                        //   * Yellow, 30px circles when point count is between 100 and 750
                        //   * Pink, 40px circles when point count is greater than or equal to 750
                        'circle-color': [
                            'step',
                            ['get', 'point_count'],
                            '#51bbd6',
                            100,
                            '#f1f075',
                            750,
                            '#f28cb1'
                        ],
                        'circle-radius': [
                            'step',
                            ['get', 'point_count'],
                            20,
                            100,
                            30,
                            750,
                            40
                        ]
                    }
                });
        
                await map.addLayer({
                    id: 'cluster-count',
                    type: 'symbol',
                    source: 'trafficLights',
                    filter: ['has', 'point_count'],
                    layout: {
                        'text-field': ['get', 'point_count_abbreviated'],
                        'text-font': ['DIN Offc Pro Medium', 'Arial Unicode MS Bold'],
                        'text-size': 12
                    }
                });
            
                await map.addLayer({
                    id: 'unclustered-point',
                    type: 'circle',
                    source: 'trafficLights',
                    filter: ['!=','cluster', true ],
                    paint: {
                        // 'circle-color': '#11b4da',
                        // 'circle-radius': 4,
                        'circle-radius':8,
                        'circle-stroke-width': 2,
                        // 'circle-stroke-color': '#fff'
                        'circle-stroke-color':'#000',
                        'circle-color': [
                            'case',
                            traffic0,
                            '#1ff042', // somewhat green 
                            traffic1,
                            '#faca1e', // somewhat orange
                            traffic2,
                            '#e00d0d', // somewhat red
                            '#11b4da'
                        ]
                    }
                });
        
                await map.on('click', 'unclustered-point', (e) => {
                    //  Traffic Number 0 / 1 / 2
                    const trafficNumber = e.features[0].properties.traffic;
                    //  Coordinates of popup
                    const coordinates = e.features[0].geometry.coordinates.slice();
                    
                    var trafficLabel = '';
                    if (trafficNumber === 0) trafficLabel = 'No traffic';
                    if (trafficNumber === 1) trafficLabel = 'Medium Traffic';
                    if (trafficNumber === 2) trafficLabel = 'High Traffic';
                    if (trafficLabel == '') trafficLabel = 'No Traffic Data Available';
                    
                    //  Sets up Pop-Up text
                    new mapboxgl.Popup().setLngLat(coordinates).setHTML(
                        trafficLabel
                    ).addTo(map);
                })
        
            })
        
        
        
        // fetchTrafficData();
        `
        document.body.append(inlineScript);
    }, [])
  return (
    <div id='map'></div>
  )
}

export default Map