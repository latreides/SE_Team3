var buttonsDisabled = false;

window.onload = function() {
    toggleButtons();
    $("#uiCard").click(flip);
};

function loadXMLDoc() {
    var xmlhttp;
    if (window.XMLHttpRequest) {// code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp=new XMLHttpRequest();
    } else {// code for IE6, IE5
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
    
    if (buttonsDisabled) {
        $("#ui5").attr("title", "Please flip the card by clicking on it before rating its difficulty.");
        $("#ui4").attr("title", "Please flip the card by clicking on it before rating its difficulty.");
        $("#ui3").attr("title", "Please flip the card by clicking on it before rating its difficulty.");
        $("#ui2").attr("title", "Please flip the card by clicking on it before rating its difficulty.");
        $("#ui1").attr("title", "Please flip the card by clicking on it before rating its difficulty.");
    } else {
        $("#ui5").attr("title", "I don't know what I'm looking at.");
        $("#ui4").attr("title", "I'm unfamiliar with this.");
        $("#ui3").attr("title", "I'm familiar with this.");
        $("#ui2").attr("title", "I'm comfortable with this.");
        $("#ui1").attr("title", "I have mastered this.");
    }
}

function flip() {
    toggleButtons();
}

function exitStageLeft() {
    // shove the current card out + left.
}