
    rendererOptions = {
        draggable: true,
        preserveViewport:false
    };
    var directionsDisplay = new google.maps.DirectionsRenderer(rendererOptions);
    var directionsService = new google.maps.DirectionsService();
    var map;


    // 中心の位置座標を指定する
    <!--新宿グランドタワー-->
    var latlng = new google.maps.LatLng(35.695803589598675 , 139.6903158724308 );

    var mapTypeId = google.maps.MapTypeId.ROADMAP

    var opts = {
        zoom: 16 ,				// ズーム値
        center: latlng ,		// 中心座標 [latlng]
        mapTypeId: mapTypeId
    };
    map = new google.maps.Map(document.getElementById('map-canvas'),opts);
    directionsDisplay.setMap(map);

    google.maps.event.addListener(directionsDisplay, 'directions_changed', function(){
    });
    // マーカーのインスタンスは配列で管理しよう
    var markers = [] ;

    // マーカーのインスタンスを作成する
    markers[0] = new google.maps.Marker({
        map: map ,
        position: latlng ,
    }) ;
