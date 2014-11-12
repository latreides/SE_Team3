var newCardCounter = 0;
var editingSide = 0; // 0 Front 1 Back

function updateText(){
    var txt = $('#cardTextContent').val();
    var cardId = $('#cardPreview').attr('data-cardId');

    var miniPreview = $('.cardMiniPreview[data-cardId="' + cardId + '"]');
    miniPreview.find('label').text(txt);

    if (editingSide == 0){
        $('#frontText-' + cardId).val(txt);
    }
    else{
        $('#backText-' + cardId).val(txt);
    }
}

function updateTheme(theme, shortName){
    $('#themeField').val(shortName);
    theme = theme.replace(' ', '%20');
    $('#cardPreview').css('background-image', 'url(' + theme +')');
    $('.cardMiniPreview').css('background-image', 'url(' + theme +')');
}

function updateCardList(){
    var newCardList = []

    $('.cardMiniPreview').each(function() {
        newCardList[newCardList.length] = $(this).attr('data-cardId');
    });

    $(cardIdList).val(newCardList.toString());

    var visibleCount = $('.cardMiniPreview:not(.cardRemoved)').length;

    $('#cardsContainer').css('width', (68*visibleCount) + 'px')

    $('#removeCard').toggle(visibleCount > 1);
}

function selectCard(card){
        var cardId = $(card).attr('data-cardId');

        if (editingSide == 0)
        {
            $('#cardTextContent').val($('#frontText-' + cardId).val());
        }
        else{
            $('#cardTextContent').val($('#backText-' + cardId).val());
        }

        $('#cardPreview').attr('data-cardId', cardId);
        $('.cardMiniPreview').removeClass('cardSelected');
        $(card).addClass('cardSelected');
}

function previewUploadedImage() {
    var input = $("#uploadImagesButton")[0];
    var img = $("#uploadImagesButton")[0].files[0];
    
    if( !(new FileReader()) ) {
        console.log("FileReader unsupported! Preview will not function.");
        return;
    }
    
    if( input.files && input.files[0] ) {
        var reader = new FileReader();
        
        reader.onload = function(e) {
            $("#uploadedImage").attr( "src", e.target.result );
            $("#imgPreviewContainer").show();
            $("#imgPreviewContainer").css("max-width", $("body").width());
            
            var offset = $("body").innerHeight()/2 - $("#imageDrawer").height()/2;
            $("#imageDrawer").css( "top", offset );
        }
        
        reader.readAsDataURL( input.files[0] );
    }
}

$(document).ready(function(){
    $('#previewContainer').on("click", ".cardMiniPreview", function(){
        selectCard($(this));
    });

    $('.themePreview').click(function(){
        $('.themePreview').removeClass('themeSelected');
        $(this).addClass('themeSelected');
        updateTheme($(this).attr('src'), $(this).attr('data-theme'));
    });

    $('#addCard').click(function(){
        var cardId = 'new_' + (newCardCounter++);
        var cardImage = $('.cardSelected').css('background-image');
        var newPreviewDiv =  $('<div class="cardMiniPreview cardMiniPreview-add" data-cardId="' + cardId + '" style="background-image:' + cardImage + '" ></div>');
        var newLabel = $('<label></label>');
        var newFrontField = $('<input  id="frontText-' + cardId  + '" type="hidden" name="front-' + cardId + '" value="">');
        var newBackField = $('<input  id="backText-' + cardId  + '" type="hidden" name="back-' + cardId + '" value="">');

        $('#cardsContainer').append($(newPreviewDiv))
        //$(newPreviewDiv).insertBefore($(this));
        $(newPreviewDiv).append(newLabel);
        $(newPreviewDiv).append(newFrontField);
        $(newPreviewDiv).append(newBackField);
        updateCardList();
    });

    $('#removeCard').click(function(){
        var reallyRemove = confirm('Remove current card?');
        if (reallyRemove == true) {
            var cardToRemove = $('.cardSelected');
            cardToRemove.fadeOut('slow' );
            cardToRemove.attr('data-cardId', '*' + cardToRemove.attr('data-cardId'));
            cardToRemove.addClass('cardRemoved');

            nextSibling = cardToRemove.next('.cardMiniPreview:not(.cardRemoved)');
            prevSibling = cardToRemove.prev('.cardMiniPreview:not(.cardRemoved)');
            if (nextSibling.length > 0) {
                selectCard(nextSibling);
            }
            else if (prevSibling.length > 0) {
                selectCard(prevSibling);
            }

            updateCardList();
        }
    });

    $('.cardSideRadio').click(function(){
        editingSide = ($(this).attr('id') == 'cardFront') ? 0 : 1;
        var cardId  = $('.cardSelected').attr('data-cardId');

        if (editingSide == 0)
        {
            $('#cardTextContent').val($('#frontText-' + cardId).val());
        }
        else{
            $('#cardTextContent').val($('#backText-' + cardId).val());
        }
    })

    $('#submitDeckChanges').click(function(){

    })

    $('#cardTextContent').change(updateText);
    $('#cardTextContent').keyup(updateText);

    $('#previewScrollLeft').click(function(){
        var container = $('#cardsContainer');
        var newLeft = (container.position().left + 64);
        if (newLeft > 0) {
            newLeft = 0;
        }
        container.css('left', newLeft + 'px');
    })

    $('#previewScrollRight').click(function(){
        var container = $('#cardsContainer');
        var newLeft = (container.position().left - 64);
        var farRight = newLeft + container.width();
        if (farRight >= $(this).position().left) {
            container.css('left', newLeft + 'px');
        }
    })
    
    $("#uploadImages").click( function() {
        $("#overlay").show();
        $("#imageDrawer").show();
        var offset = $("body").innerHeight()/2 - $("#imageDrawer").height()/2;
        $("#imageDrawer").css( "top", offset );
    });
    
    $("#cancelUpload").click( function() {
        $("#overlay").hide();
        $("#imageDrawer").hide();
        $("#imgPreviewContainer").hide();
    });
    
    $("#overlay").click( function() {
        $("#overlay").hide();
        $("#imageDrawer").hide();
        $("#imgPreviewContainer").hide();
    });
    
    $(window).resize( function() {
        var offset = $("body").innerHeight()/2 - $("#imageDrawer").height()/2;
        $("#imageDrawer").css( "top", offset );
    });
    
    $("#uploadImagesButton").change( previewUploadedImage );

    updateCardList();
});
