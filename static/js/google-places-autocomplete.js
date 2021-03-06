function autocomplete_start() {
	var input = document.getElementById("id_start_address");
	var options = {
		types: ['establishment'],
		componentRestrictions: {country: 'jp'}
		};
	var autocomplate_start = new google.maps.places.Autocomplete(input, options);
	autocomplate_start.addListener('place_changed', function() {
		var place = autocomplate_start.getPlace();
		document.getElementById("id_start_address").value = place.name;
		document.getElementById("id_start_address2").value = place.formatted_address;
		document.getElementById("id_start_location").value = place.geometry.location;
	});
}
function autocomplete_arriv() {
	var input = document.getElementById("id_arriv_address");
	var options = {
		types: ['establishment'],
		componentRestrictions: {country: 'jp'}
		};
	var autocomplate_arriv = new google.maps.places.Autocomplete(input, options);
	autocomplate_arriv.addListener('place_changed', function() {
		var place = autocomplate_arriv.getPlace();
		document.getElementById("id_arriv_address").value = place.name;
		document.getElementById("id_arriv_address2").value = place.formatted_address;
		document.getElementById("id_arriv_location").value = place.geometry.location;
	});
}
google.maps.event.addDomListener(window, 'load', autocomplete_start);
google.maps.event.addDomListener(window, 'load', autocomplete_arriv);