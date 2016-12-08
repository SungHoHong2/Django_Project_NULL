
var markers = [];
var map;
var geocoder;

function setText(val, e) {
    document.getElementById(e).value = val;
}
function insertText(val, e) {
    document.getElementById(e).value += val;
}

var nav = null;
var watchID;
function listenForPosition() {
  geocoder = new google.maps.Geocoder();

  if (nav == null) {
      nav = window.navigator;
  }
  if (nav != null) {
      var geoloc = nav.geolocation;
      if (geoloc != null) {
          watchID = geoloc.watchPosition(successCallback, errorCallback)

          geoloc.watchPosition(function (pos) {

      			// 현재 위경도 값(GPS) 변수에 넣기.
      			var latitude = pos.coords.latitude;
      			var longitude = pos.coords.longitude;

      			var mapOptions = {
      				zoom: 16,
      				mapTypeId: google.maps.MapTypeId.ROADMAP,
      				center: new google.maps.LatLng(latitude,longitude)
      			};

      			map = new google.maps.Map(document.getElementById('map'),mapOptions);

      			// 현재 위치 마커 생성
      			var marker = new google.maps.Marker({
      				position: new google.maps.LatLng(latitude,longitude),
      				map: map,
      				draggable: false,
      				icon: "http://maps.google.com/mapfiles/ms/micons/man.png"
      			});

      			markers.push(marker);

      			// 현재 위치 기준 원 그리기
      			var populationOptions = {
      				strokeColor: '#000000',
      				strokeOpacity: 0.8,
      				strokeWeight: 2,
      				fillColor: '#808080',
      				fillOpacity: 0.5,
      				map: map,
      				center: new google.maps.LatLng(latitude,longitude) ,
      				radius: 1000
      			};

      			cityCircle = new google.maps.Circle(populationOptions);

      			var script = document.createElement('script');
      			// This example uses a local copy of the GeoJSON stored at
      			// http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_week.geojsonp
      			//script.src = './data.js';
      			document.getElementsByTagName('head')[0].appendChild(script);
        });
      }
      else {
          console.log("Geolocation not supported");
      }
  }
  else {
      console.log("Navigator not found");
  }
}
function clearWatch(watchID) {
    window.navigator.geolocation.clearWatch(watchID);
}
function successCallback(position)
{
   //setText(position.coords.latitude, "latitude");
   //setText(position.coords.longitude, "longitude");
}


function errorCallback(error) {
    var message = "";
    // Check for known errors
    switch (error.code) {
        case error.PERMISSION_DENIED:
            message = "This website does not have permission to use " +
                      "the Geolocation API";
            break;
        case error.POSITION_UNAVAILABLE:
            message = "The current position could not be determined.";
            break;
        case error.PERMISSION_DENIED_TIMEOUT:
            message = "The current position could not be determined " +
                      "within the specified timeout period.";
            break;
    }
    // If it's an unknown error, build a message that includes
    // information that helps identify the situation so that
    // the error handler can be updated.
    if (message == "")
    {
        var strErrorCode = error.code.toString();
        message = "The position could not be determined due to " +
                  "an unknown error (Code: " + strErrorCode + ").";
    }
    console.log(message);
}

window.friends_callback = function(results) {
	for (var i = 0; i < results.features.length; i++) {
		var coords = results.features[i].geometry.coordinates;
		var latLng = new google.maps.LatLng(coords[0],coords[1]);
		var marker = new google.maps.Marker({
			position: latLng,
			map: map
		});
	}
}

$( window ).load(function() {
	listenForPosition();
});
