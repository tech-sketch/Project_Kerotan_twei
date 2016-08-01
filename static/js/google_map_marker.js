    function CreateMarker(latlng){
       var marker = new google.maps.Marker({
            position: latlng,
            map: map,
            label: {
                text: 'V',
                <!--color: 'purple'-->
            }
            <!--draggable: true-->
        });
        <!--google.maps.event.addListener(marker, 'dragend', UpdateRoute);-->
        return marker;
    }

    function CreateMarkerStart(latlng){
        var marker = new google.maps.Marker({
            <!--icon: icon,-->
            position: latlng,
            map: map,
            label: {
                text: 'S',
                color: 'white',
                <!--fontSize: '30'-->
            }
            <!--draggable: true-->
        });
        <!--google.maps.event.addListener(marker, 'dragend', UpdateRoute);-->
        return marker;
    }

    function CreateMarkerEnd(latlng){
        var marker = new google.maps.Marker({
            position: latlng,
            map: map,
            label: {
                text: 'E',
                color: 'white'
            }
            <!--draggable: true-->
        });
        <!--google.maps.event.addListener(marker, 'dragend', UpdateRoute);-->
        return marker;
    }

