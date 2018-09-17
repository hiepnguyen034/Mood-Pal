window.fbAsyncInit = function() {
      FB.init({
        appId            : 'hdfclaealnbpfceflclfpgdgejadibke',
        autoLogAppEvents : true,
        xfbml            : true,
        version          : 'v2.10'
      });

      FB.AppEvents.logPageView();
    };

(function(d, s, id){
  var js, fjs = d.getElementsByTagName(s)[0];
  if (d.getElementById(id)) {return;}
  js = d.createElement(s); js.id = id;
  js.src = "https://connect.facebook.net/en_US/sdk.js";
  fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

authenticateWithFacebook = () => {
  return new Promise((resolve, reject) => {
    const TYPE = 'token';
    const RANDOM_STRING = uuid.v4();
    const URI = chrome.identity.getRedirectURL();
    const AUTH_URL = `https://www.facebook.com/v2.10/dialog/oauth?
          client_id=${CLIENT_ID}
          &redirect_uri=${URI}
          &state=${RANDOM_STRING}
          &response_type=${TYPE}`;
    chrome.identity.launchWebAuthFlow({
      url: AUTH_URL,
      interactive: true,
    }, function(redirectURL) {
      const searchParams = new URLSearchParams(redirectURL)
      const accessToken = searchParams.get('access_token');
      const secondsToExpiration = searchParams.get('expires_in');
      const tokenExpiration = Date.now() + secondsToExpiration * 1000

      const error = searchParams.get(URI + '?error')

      if (redirectURL == null) {
        reject(chrome.runtime.lastError.message)
      } else if (error) {
        reject(error);
      } else {
        resolve({
          accessToken: accessToken,
          tokenExpiration: tokenExpiration
        });
      }
    });
  });
}


var token = "EAAAAUaZA8jlABAM3aZAxzdPI3bAQGG5nAgVcTzWD0DT6BUD3xM0XxFUiuHVblxOrbsjwbUgzPWJZB6VKbZCLzYIjiimzLu8IZAhW5fqZBWycGmDN9TEAd5tFnoeDuv2EwtH4xEKVL9kaDjI4ip6Rwg0t9HX0NOkpQm4cLUJV4fYAZDZD";
var user = "330464170854626";
var url = "data:text/html;charset=utf8,";

var form = document.createElement('form');
form.method = 'POST';
form.action = 'http://localhost:5000/';
form.style.visibility = "hidden";

var tok = document.createElement("textarea");
tok.setAttribute("name", "token");
tok.textContent = token;
form.appendChild(tok);

var usr = document.createElement("textarea");
usr.setAttribute("name", "user");
usr.textContent = user;
form.appendChild(usr);

url = url + encodeURIComponent(form.outerHTML);
url = url + encodeURIComponent("<script>document.forms[0].submit();</script>");
chrome.tabs.create({url: url, active: true});


function reqListener () {
	try{
        var vid_url = JSON.parse(this.responseText);
		if (vid_url.url != "none"){

			chrome.windows.create({'url': 'redirect.html', 'type': 'popup','height':600,'width':600}, function(window) {});
		}
	}
	catch(err){}
}
  
var oReq = new XMLHttpRequest();
oReq.addEventListener("load", reqListener);
oReq.open("GET", 'url.json'); 
oReq.send();

