function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for(var i = 0; i <ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function getXMLHttpRequest() {
	var xhr = null;

	if (window.XMLHttpRequest || window.ActiveXObject) {
		if (window.ActiveXObject) {
			try {
				xhr = new ActiveXObject("Msxml2.XMLHTTP");
			} catch(e) {
				xhr = new ActiveXObject("Microsoft.XMLHTTP");
			}
		} else {
			xhr = new XMLHttpRequest();
		}
	} else {
		alert("Votre navigateur ne supporte pas l'objet XMLHTTPRequest...");
		return null;
	}

	return xhr;
}

function restLoad(requestURL,func,...args) {
  var request = getXMLHttpRequest();
  request.open("GET", requestURL, true);
  request.responsetype = 'Json';
  request.send();
  request.onload = function() {
		func(JSON.parse(request.response),args);
		//return JSON.parse(request.response);
  }
}

function restSend(requestURL,mode,jsonData) {
  var request = getXMLHttpRequest();
  request.open(mode, requestURL, true);
  request.setRequestHeader('Content-Type', 'application/json');
	request.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
  response=request.send(jsonData);
	return response;
}

function pageLoad(requestURL,func,...args) {
  var request  = getXMLHttpRequest();
  request.open("GET", requestURL, true);
  request.send();
  request.onload = function() {
    var response=request.responseText.replace(/^\s*$(?:\r\n?|\n)/gm,"");
    func(response,args);
  }
}
