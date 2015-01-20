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

function getEventFilenames() {
    var url = "/api/eventfilenames";
    var client = new XMLHttpRequest();
    client.open("GET", url, false);
    client.setRequestHeader("Content-Type", "text/plain");
    client.send();
    var response = [];
    if (client.status == 200) {
        response = JSON.parse(client.responseText);
    }
    return(response);
}


var imageFiles = getEventFilenames();
var imageIndexMin = 0;
var imageIndexMax = imageFiles.length - 1;
var imageIndex = imageIndexMax;

function changeImage(i) {
    document.getElementById("piclink").href="/events/"+imageFiles[i];
    document.getElementById("previewpic").src="/events/"+imageFiles[i];
    document.getElementById("dllink").href="/events/"+imageFiles[i];
    document.getElementById("dllink").download=imageFiles[i];
    document.getElementById("dllink").innerHTML=imageFiles[i];
}

document.onkeydown = function(event) {
    event = event || window.event;

    switch (event.keyCode || event.which) {
        case 37:
            //left
            imageIndex = imageIndex + 1;
            if (imageIndex > imageIndexMax) {
                imageIndex = imageIndexMin;
            }
            changeImage(imageIndex);
            break;
        case 39:
            //right
            imageIndex = imageIndex - 1;
            if (imageIndex < 0) {
                imageIndex = imageIndexMax;
            }
            changeImage(imageIndex);
            break;
    }
};

function refresh() {
    oldImageIndexMax = imageIndexMax;
    imageFiles = getEventFilenames();
    imageIndexMin = 0;
    imageIndexMax = imageFiles.length - 1;
    if (imageIndex == oldImageIndexMax) {
        imageIndex = imageIndexMax;
        changeImage(imageIndex);
    }
    document.getElementById("freespace").innerHTML = "free space: " + getFreeSpace()
    document.getElementById("camerastatus").innerHTML = getCameraStatus()
}


var refreshInterval = setInterval( "refresh()", 5 * 1000);

//initial values on page load
changeImage(imageIndexMax);
document.getElementById("freespace").innerHTML="free space: " + getFreeSpace()
document.getElementById("camerastatus").innerHTML = getCameraStatus()
