function getAjax(_type, _url, _contentType, _success){
   send_request = {
            type: _type
            , async : true
            , url : _url
            , contentType: _contentType
            , error : function(request, status, error) {
                alert("code : " + request.status + "\r\n장애가 발생하였습니다.");
            }
            , success : _success
   }

  $.ajax(send_request);
}


function postAjax(_type, _data, _url, _contentType, _success){
  $.ajax({
          type: _type
         , beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
        , url : _url
        , data : _data
        , contentType: _contentType
        , error : function(request, status, error) {
            alert("code : " + request.status + "\r\n장애가 발생하였습니다.");
        }
        , success : _success
        });
}


function formAjax(_type, _data, _url, _contentType, _success){

  $.ajax({
          type: _type
         , beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
        , url : _url
        , data : _data
		, processData: false
		, contentType: false
		, error : function(request, status, error) {
            alert("code : " + request.status + "\r\n장애가 발생하였습니다.");
        }
        , success : _success
        });

}


function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function openModal(){

		// Get the modal
		var modal = document.getElementById('myModal');

		// Get the button that opens the modal
		var btn = document.getElementById("myBtn");

		// Get the <span> element that closes the modal
		var span = document.getElementsByClassName("close")[0];

		// When the user clicks the button, open the modal
		btn.onclick = function() {
			modal.style.display = "block";
		}

		// When the user clicks on <span> (x), close the modal
		span.onclick = function() {
			modal.style.display = "none";
		}

		// When the user clicks anywhere outside of the modal, close it
		window.onclick = function(event) {
			if (event.target == modal) {
				modal.style.display = "none";
			}
		}

}
