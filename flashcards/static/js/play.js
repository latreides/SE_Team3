var cardHasBeenFlipped = false;
var buttonsDisabled = false;
var showingFront    = true;

var settingsOpen = false;
var helpOpen     = false;
var showingHelpSection = [false, false, false, false];

var orderOptions = ["frontFirst", "backFirst", "random"];
var order = orderOptions[0];

window.onload = function() {
    toggleButtons();
    $("#uiCard").click(flip);
    $("#uiSettingsButton").click(toggleSettingsDrawer);
    $("#uiHelpButton").click(toggleHelpDrawer);
    
    $("#ui1").hover(rollIconDown, rollIconUp);
    $("#ui2").hover(rollIconDown, rollIconUp);
    $("#ui3").hover(rollIconDown, rollIconUp);
    $("#ui4").hover(rollIconDown, rollIconUp);
    $("#ui5").hover(rollIconDown, rollIconUp);
    
    $("#uiSkip").hover(rollIconDown, rollIconUp);
    
    $("#whatDoIDoT").click(showHelpSection);
    $("#movingBetweenCardsT").click(showHelpSection);
    $("#shortcutsT").click(showHelpSection);
    $("#settingsT").click(showHelpSection);
};

// disable space bar scrolling
window.onkeydown = function(event) {
    return !(event.keyCode == 32);
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

function toggleSettingsDrawer() {
    if (settingsOpen) {
        $("#uiSettingsButton").removeClass("settingsOpen");
        $("#uiSettingsDrawer").slideUp("fast");
    } else {
        $("#uiSettingsButton").addClass("settingsOpen");
        $("#uiSettingsDrawer").slideDown("fast");
    }
    settingsOpen = !settingsOpen;
}

function toggleHelpDrawer() {
    if (helpOpen) {
        $("#uiHelpButton").removeClass("helpOpen");
        $("#uiHelpDrawer").slideUp("fast");
    } else {
        $("#uiHelpButton").addClass("helpOpen");
        $("#uiHelpDrawer").slideDown("fast");
    }
    helpOpen = !helpOpen;
}

function rollIconDown() {
    var index = parseInt( $(this).attr("data-id") );
    if (!cardHasBeenFlipped && index != 6)
        return;
    
    switch (index) {
        case 1: $("#uiBtnIcon1").slideDown("fast"); break;
        case 2: $("#uiBtnIcon2").slideDown("fast"); break;
        case 3: $("#uiBtnIcon3").slideDown("fast"); break;
        case 4: $("#uiBtnIcon4").slideDown("fast"); break;
        case 5: $("#uiBtnIcon5").slideDown("fast"); break;
        case 6: $("#uiBtnIconSkip").slideDown("fast"); break;
    }
}
function rollIconUp() {
    var index = parseInt( $(this).attr("data-id") );
    switch (index) {
        case 1: $("#uiBtnIcon1").slideUp("fast"); break;
        case 2: $("#uiBtnIcon2").slideUp("fast"); break;
        case 3: $("#uiBtnIcon3").slideUp("fast"); break;
        case 4: $("#uiBtnIcon4").slideUp("fast"); break;
        case 5: $("#uiBtnIcon5").slideUp("fast"); break;
        case 6: $("#uiBtnIconSkip").slideUp("fast"); break;
    }
}

function showHelpSection() {
    var index = parseInt( $(this).attr("data-helpID") );
    
    if ( showingHelpSection[index] ) {
        showingHelpSection[index] = false;
        switch (index) {
            case 0:
                $("#whatDoIDoD").slideUp("fast");
                return;
            case 1:
                $("#movingBetweenCardsD").slideUp("fast");
                return;
            case 2:
                $("#shortcutsD").slideUp("fast");
                return;
            case 3:
                $("#settingsD").slideUp("fast");
                return;
        }
    }
    
    for( var i = 0; i < showingHelpSection.length; i += 1 ) {
        showingHelpSection[i] = false;
    }
    showingHelpSection[index] = true;
    
    switch (index) {
        case 0:
            $("#whatDoIDoD").slideDown("fast");
            $("#movingBetweenCardsD").slideUp("fast");
            $("#shortcutsD").slideUp("fast");
            $("#settingsD").slideUp("fast");
            break;
        case 1:
            $("#whatDoIDoD").slideUp("fast");
            $("#movingBetweenCardsD").slideDown("fast");
            $("#shortcutsD").slideUp("fast");
            $("#settingsD").slideUp("fast");
            break;
        case 2:
            $("#whatDoIDoD").slideUp("fast");
            $("#movingBetweenCardsD").slideUp("fast");
            $("#shortcutsD").slideDown("fast");
            $("#settingsD").slideUp("fast");
            break;
        case 3:
            $("#whatDoIDoD").slideUp("fast");
            $("#movingBetweenCardsD").slideUp("fast");
            $("#shortcutsD").slideUp("fast");
            $("#settingsD").slideDown("fast");
            break;
    }
}

function rate(rating) {
    
}

function exitStageLeft() {
    // shove the current card out + left.
    cardHasBeenFlipped = false;
}