
var markers = [];
var marker2 =[];
var map;
var geocoder;
var infowindow = null;
var latitude = 0;
var longitude = 0;


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
                var location = latitude.toString() + "," + longitude.toString()
				postAjax('PUT', {'location': location}, '/member/member_position/'
					, 'application/x-www-form-urlencoded', function(response){
					    $('#alert_location').remove();
                        $('.search-view').append($('<span/>').attr('id','alert_location').text('지역 위치를 저장하고 있습니다.'));
                        $( "#alert_location" ).animate({ opacity: 0, height: 0}, 3000, function() {
					                         $(this).hide();
                         });


				});


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

                viewMarker();

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
   setText(position.coords.latitude, "latitude");
   setText(position.coords.longitude, "longitude");
}

function viewMarker() {
        console.log('viewMarker activated');
        $('.member-info').css({'background': ''});

        var infowindow = new google.maps.InfoWindow();
        marker2 = [];
        for (var i = 0; i < google_data.features.length; i++) {

                    var _member_id = google_data.features[i].member_id;
                    var coords = google_data.features[i].geometry.coordinates;
                    var latLng = new google.maps.LatLng(coords[0],coords[1]);
                    var marker = new google.maps.Marker({
                        member_id : google_data.features[i].member_id,
                        position: latLng,
                        map: map,
                        icon: 'https://null-bucket.s3.amazonaws.com/static/base_dev/images/default_icon.png'
                    });

                    marker2.push(marker);
        }


        $(marker2).each(function(index, item){

                 item.addListener('click',function() {


                       $(marker2).each(function(index_2, item_2){
                              item_2.setIcon('https://null-bucket.s3.amazonaws.com/static/base_dev/images/default_icon.png');
                       });

                       $('.member-info').css({'background': ''});
                       item.setIcon('https://null-bucket.s3.amazonaws.com/static/base_dev/images/clicked_icon.png');
                       console.log(item.member_id);
                       $('#'+item.member_id).parent().css({'background': 'green'});
                 });

        })


}

function fnRemoveMarker(){
     console.log('before delete');
     console.log(marker2);
	for (var i = 0; i < google_data.features.length; i++) {
		marker2[i].setMap(null);
	}
     console.log('after delete');
	 console.log(marker2);

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

$( window ).load(function() {
	listenForPosition();
});
