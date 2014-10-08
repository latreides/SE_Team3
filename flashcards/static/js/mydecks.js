var drawerVis = false;

function drawerSlide() {
    if(!drawerVis) {
        $("#deckDrawer").slideDown();
        drawerVis = true;
    }
}
function closeDrawer() {
    $("#deckDrawer").slideUp();
    drawerVis = false;
}

function updateDeckDrawer(child) {
    /**
    When a deck is clicked, update
    the deck drawer to reflect the
    info specific to the deck in
    question.
    */
    titleBar = $("#dTitle");
    desc = $("#desc");
    count = $("#cardCount");
    acc = $("#access");
    auth = $("#author");

    titleBar.html($(this).attr("data-deckName") );
    desc.html($(this).attr("data-deckDesc") );
    count.html($(this).attr("data-cardCount") );
    acc.html( $(this).attr("data-lastAccess") );
    auth.html( $(this).attr("data-author") );
}

window.onload = function() {
        $(".manage").click( drawerSlide      );
        $(".manage").click( updateDeckDrawer );
        $("#closeButton").click( closeDrawer );
    };
