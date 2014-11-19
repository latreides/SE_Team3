var cardHasBeenFlipped = false;
var buttonsDisabled    = true;
var showingFront       = true;

var settingsOpen = false;
var helpOpen     = false;
var showingHelpSection = [false, false, false, false];

var orderOptions = ["frontFirst", "backFirst", "random"];
var order = orderOptions[0];

var ratingToSend = 6;

/* ===== Color Fading Settings for flashcard content and buttons =====
 * Elements to flash upon click:
 *  - Difficulty buttons (data-ids 1 - 5, array indices 0 - 4, from Very Easy to Very Hard)
 *  - Skip button (data-id 6, array index 5)
 *  - Front and back side of flashcard (data-ids 7 and 8, array indices 6 and 7)
 */
var duration   = 500;
var flashColor = [255, 255, 255, 1];
//      the colors the buttons start with
var originalColors = [];
//      interpolation multiplier, 1 == 100%; affects color blending
var im = 1;
//      amount of fade left for each flash-able element
var fadeDuration  = [im, im, im, im, im, im];
//      container for JS interval objects for fading, per flash-able element
var fadeInterval  = [null, null, null, null, null, null];
//      how often to perform fade effect in milliseconds
var fadeFrequency = 10;
//      percentage to decrement from fade remaining
var tick = 0.04; // fadeFrequency / duration;
/* ===== End Color Fading Settings ===== */

$(document).ready(function() {
    $("#uiSettingsButton").click(toggleSettingsDrawer);
    $("#uiHelpButton").click(toggleHelpDrawer);
    
    populateOriginalColors();
    
    $("#ui1").hover(rollIconDown, rollIconUp).click(flashButton).click(getNextCard);
    $("#ui2").hover(rollIconDown, rollIconUp).click(flashButton).click(getNextCard);
    $("#ui3").hover(rollIconDown, rollIconUp).click(flashButton).click(getNextCard);
    $("#ui4").hover(rollIconDown, rollIconUp).click(flashButton).click(getNextCard);
    $("#ui5").hover(rollIconDown, rollIconUp).click(flashButton).click(getNextCard);
    $("#uiCard").click(flip);
    $("#flipHotkey").click(flip);
    
    $("#uiSkip").hover(rollIconDown, rollIconUp).click(flashButton).click(getNextCard);
    
    $("#whatDoIDoT").click(showHelpSection);
    $("#movingBetweenCardsT").click(showHelpSection);
    $("#shortcutsT").click(showHelpSection);
    $("#settingsT").click(showHelpSection);
    
    // this is somewhat of a bandaid for the card text not appearing right
    //   away but maintaining the desired fade on click/keyup events.
    $("#uiCardFront").fadeIn();
});

// disable space bar scrolling and F1 showing browser help
window.onkeydown = function(event) {
    return !(event.keyCode == 32 || event.keyCode == 112);
};

document.addEventListener( "keyup", function(event) {        
        switch (event.keyCode) {
            case 37: // left arrow key
            case 39: // right arrow key
                $("#uiSkip").trigger("click");
                break;
                
            case 32: // space bar
                $("#uiCard").trigger("click");
                break;
                
            case 49: // Number row: 1
                $("#ui1").trigger("click");
                break;
                
            case 50: // Number row: 2
                $("#ui2").trigger("click");
                break;
                
            case 51: // Number row: 3
                $("#ui3").trigger("click");
                break;
                
            case 52: // Number row: 4
                $("#ui4").trigger("click");
                break;
                
            case 53: // Number row: 5
                $("#ui5").trigger("click");
                break;
                
            case 112: // F1 key
            case 191: // ?  key
                $("#uiHelpButton").trigger("click");
                break;
                
            /* default:
                console.log(event.keyCode);
                break;
            */
        }
    }
);

// Need to redo in JQuery with correct URL
function loadXMLDoc(deckId) {
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
            document.getElementById("myDiv").innerHTML="<h4>" + xmlhttp.responseText + "</h4>";
        } else if (xmlhttp.readyState == 4 && xmlhttp.status == 404) {
            document.getElementById("myDiv").innerHTML = "<h4><em>404 - Not Found. Did you forget the argument?</em></h4>";
        } else if (xmlhttp.readyState == 4 && xmlhttp.status == 500) {
            document.getElementById("myDiv").innerHTML = 
                "<h4><em>500 - No deck with ID [" + String(deckId) + "] was found.</em></h4>";
        } else {
            document.getElementById("myDiv").innerHTML = "<h4>Loading...</h4>";
        }
    }
    xmlhttp.open("GET","/getNextCard/" + String(deckId),true);
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
    
    $("#uiCardFront").css("display", "none");
    $("#uiCardBack").css("display", "none");
    if (showingFront)
        $("#uiCardBack").fadeIn();
    else
        $("#uiCardFront").fadeIn();
    
    showingFront = !showingFront;
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

function populateOriginalColors() {
    toggleButtons();
    var col0 = $("#ui1").css("background-color").replace(/[^\d,]/g,'').split(',');
    var col1 = $("#ui2").css("background-color").replace(/[^\d,]/g,'').split(',');
    var col2 = $("#ui3").css("background-color").replace(/[^\d,]/g,'').split(',');
    var col3 = $("#ui4").css("background-color").replace(/[^\d,]/g,'').split(',');
    var col4 = $("#ui5").css("background-color").replace(/[^\d,]/g,'').split(',');
    var col5 = $("#uiSkip").css("background-color").replace(/[^\d,]/g,'').split(',');
    toggleButtons();
    
    var text = $("#uiCardFront").css("color").replace(/[^\d,]/g,'').split(',');
    
    originalColors = [col0, col1, col2, col3, col4, col5];
}

function flashButton() {
    id = $(this).attr("id");
    var index = parseInt($("#" + id).attr("data-id")) - 1;
    
    if (cardHasBeenFlipped || id == "uiSkip") {
        if( id != "uiCardFront" && id != "uiCardBack" )
            initColorFadeButton( id, flashColor, "background-color" );
        else
            initColorFadeButton( id, textFade, "color" );
    }
}

function initColorFadeButton(id, toColor, attr) {
    /*
        Fade element with ID id from it's current color to toColor
    */
    var index = parseInt($("#" + id).attr("data-id")) - 1;
    
    if( fadeDuration[index] != im )
        return;
        
    fadeInterval[index] = setInterval( function(){
            var fromColor = $("#" + id).css(attr).replace(/[^\d,]/g,'').split(',');
            colorFadeButton(id, toColor, originalColors[index], attr);
        }, fadeFrequency );
}

function colorFadeButton(id, from, to, attr) {
    /*
        Fades the color of CSS Attribute 'attr' in element with id 'id' from color 'from' to color 'to.'
        Color arrays 'from' and 'to' must be in the form:
            [R,G,B[,A]] where R,G,B == int[0 ~ 255] and A == float[0 ~ 1].
            If no alpha is present, 1 is assumed.
    */
    var index = parseInt($("#" + id).attr("data-id")) - 1;
    
    from[3] = from[3] == undefined ? 1 : from[3];
    to[3]   =   to[3] == undefined ? 1 : to[3];
    
    if(fadeDuration[index] >= 0) {
        var diffInCol1 = [];
        diffInCol1[0] = from[0] - to[0];
        diffInCol1[1] = from[1] - to[1];
        diffInCol1[2] = from[2] - to[2];
        diffInCol1[3] = from[3] - to[3];
        
        var nextCol1 = [];
        nextCol1[0] = Math.floor(from[0] - (1-fadeDuration[index]) * diffInCol1[0]);
        nextCol1[1] = Math.floor(from[1] - (1-fadeDuration[index]) * diffInCol1[1]);
        nextCol1[2] = Math.floor(from[2] - (1-fadeDuration[index]) * diffInCol1[2]);
        nextCol1[3] = from[3] - (1-fadeDuration[index]) * diffInCol1[3];
        
        $("#"+id).css(attr, 
            "rgba(" + nextCol1[0] + "," + nextCol1[1] + "," + nextCol1[2] + "," + 
            nextCol1[3] + ")");
        fadeDuration[index] -= tick;
    } else {
        clearInterval(fadeInterval[index]);
        fadeDuration[index] = im;
        $("#" + id).css(attr, "");
    }
}

function getNextCard() {
    var passRating = true;
    var card = {};
    
    if( $(this).attr("data-id") != 6 && !cardHasBeenFlipped )
        return;
    
    if ( $(this).attr("data-id") == 6 ) { 
        passRating = false;
    }
    var data = {};
    data["deckId"] = $("#formDeckId").val();
    data["csrfmiddlewaretoken"] = $("input[name=csrfmiddlewaretoken]").val();
    if(passRating)
        data["rating"] = $(this).attr("data-id");
    var dataType = "json";
    var response = $.post("/getNextCard", data, dataType);
    response.done( function(cardJson) {
        card = $.parseJSON(cardJson);
        $("#uiCFT").html( card.frontText );
        $("#uiCBT").html( card.backText );
        
        // console.log( card );
    });
    
    if( !buttonsDisabled )
        toggleButtons();
    if( !showingFront )
        flip();
    cardHasBeenFlipped = false;
}