var cardHasBeenFlipped = false;
var buttonsDisabled = false;
var showingFront    = true;

var orderOptions = ["frontFirst", "backFirst", "random"];
var order = orderOptions[0];

window.onload = function() {
    toggleButtons();
    $("#uiCard").click(flip);
};

document.addEventListener( "keyup", function(event) {
        if( event.keyCode == 37 || event.keyCode == 39 || event.keyCode == 32 ||
            event.keyCode == 49 || event.keyCode == 50 || event.keyCode == 51 ||
            event.keyCode == 52 || event.keyCode == 53 ) {
            // left, right, space,
            // 1, 2, 3,
            // 4, 5 (number row)
            if (event.keyCode == 32) {
                flip();
            }
        }
    }
);

function loadXMLDoc() {
    var xmlhttp;
    if (window.XMLHttpRequest) {
        // code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp=new XMLHttpRequest();
    } else {
        // code for IE6, IE5
        xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.onreadystatechange=function() {
        if (xmlhttp.readyState==4 && xmlhttp.status==200) {
            document.getElementById("myDiv").innerHTML="<h2>" + xmlhttp.responseText + "</h2>";
        } else if (xmlhttp.readyState == 4 && xmlhttp.status == 404) {
            document.getElementById("myDiv").innerHTML = "<em>404 - Not Found...?</em>";
        } else {
            document.getElementById("myDiv").innerHTML = "Loading...";
        }
    }
    xmlhttp.open("GET","../static/info.txt",true);
    xmlhttp.send();
}

function toggleButtons() {
    buttonsDisabled = !buttonsDisabled;
    $("#ui5").toggleClass("uiButton").toggleClass("uiButtonDisabled");
    $("#ui4").toggleClass("uiButton").toggleClass("uiButtonDisabled");
    $("#ui3").toggleClass("uiButton").toggleClass("uiButtonDisabled");
    $("#ui2").toggleClass("uiButton").toggleClass("uiButtonDisabled");
    $("#ui1").toggleClass("uiButton").toggleClass("uiButtonDisabled");
}

function flip() {
    if (!cardHasBeenFlipped)
        toggleButtons();
    cardHasBeenFlipped = true;
    showingFront = !showingFront;
    $("#uiCardFront").toggleClass("hide")
    $("#uiCardBack").toggleClass("hide")
}

function rate(rating) {
    
}

function exitStageLeft() {
    // shove the current card out + left.
    cardHasBeenFlipped = false;
}