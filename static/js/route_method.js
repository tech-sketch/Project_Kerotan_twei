     //電車による移動時のルート表示(ただし、直線)
    function root_line(origin,destination){
        latlngs = [
          origin,
         destination
        ];
        var Path = new google.maps.Polyline({
            path: latlngs,
            strokeOpacity: 1.0,
            strokeColor:'#00ff00',
        });
        Path.setMap(map);
    }



    //徒歩のときのルート表示
    function root(origin,destination){
        var request = {
            origin: origin,
            destination: destination,
            <!--travelMode: google.maps.DirectionsTravelMode.TRANSIT,-->
            travelMode: google.maps.DirectionsTravelMode.WALKING,
            unitSystem: google.maps.DirectionsUnitSystem.METRIC,
            <!--optimizeWaypoints: true,-->
            <!--avoidHighways: false,-->
            <!--avoidTolls: false,-->
            <!--waypoints :wayPoints-->
        };
        rendererOptions = {
            draggable: true,
            preserveViewport:false,
            suppressMarkers : true,
        };
        directionsService.route(request,function(response,status){
            if (status == google.maps.DirectionsStatus.OK){
                 var directionsDisplay = new google.maps.DirectionsRenderer(rendererOptions);
                 directionsDisplay.setDirections(response);
                 directionsDisplay.setRouteIndex(0);
                 directionsDisplay.setMap(map);
            }
        });

    }