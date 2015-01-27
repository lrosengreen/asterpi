function getFreeSpace() {
    var url = "/api/freespace";
    var client = new XMLHttpRequest();
    client.open("GET", url, false);
    client.setRequestHeader("Content-Type", "text/plain");
    client.send();
    var response = 0;
    if (client.status == 200) {
        response = JSON.parse(client.responseText);
    }
    return(response.toFixed(2) + " GB");
}

function refresh() {
  fn = "preview.jpg?" + new Date().getTime();
  document.getElementById("piclink").href="/events/" + fn;
  document.getElementById("previewpic").src="/events/" + fn;
  document.getElementById("dllink").href="/events/" + fn;
  document.getElementById("dllink").download=fn;
  document.getElementById("dllink").innerHTML="preview.jpg";
  document.getElementById("freespace").innerHTML = "free space: " + getFreeSpace()
}


var refreshInterval = setInterval( "refresh()", 5.5 * 1000);

//initial values on page load
refresh();
