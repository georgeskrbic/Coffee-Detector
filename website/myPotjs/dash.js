$(document).ready(function () {
	var ref = new Firebase("https://blinding-heat-3035.firebaseio.com/user");
	window.setInterval(function(){
		ref.once("value", function(snapshot) {
		var data = snapshot.val();
		console.log(data.one);	
		document.getElementById("p1").innerHTML = data.one + "%";
  		});  		
	}, 5000);

	$(document).ready(function() {
		 navigator.geolocation.getCurrentPosition(function(position) {
		    loadWeather(position.coords.latitude+','+position.coords.longitude); //load weather using your lat/lng coordinates
		});
	});

	function loadWeather(location, woeid) {
	  $.simpleWeather({
	    location: location,
	    woeid: woeid,
	    unit: 'f',
	    success: function(weather) {
	    	document.getElementById("weather").innerHTML = "Temp Outside: " + weather.temp + "&deg;" + weather.units.temp;
	    	document.getElementById("location").innerHTML = "Location: " + weather.city + ", "  + weather.region;
			
			// html = '<h2><i class="icon-'+weather.code+'"></i> '+weather.temp+'&deg;'+weather.units.temp+'</h2>';
			// html += '<ul><li>'+weather.city+', '+weather.region+'</li>';
			// html += '<li class="currently">'+weather.currently+'</li>';
			// html += '<li>'+weather.alt.temp+'&deg;C</li></ul>';  
	      
	    },
	    error: function(error) {
	      $("#weather").html('<p>'+error+'</p>');
	    }
	  });
	}

});
