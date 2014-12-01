var newCardCounter = 0;
var editingSide = 0; // 0 Front 1 Back

function img_upload_completed()
{
    var url = $('#upload-target').contents().find('body').text();
    if (url != 'failure')
    {
        $('#cardImageContent').attr('src', '/media/' + url);
        $('#cardTextContent').addClass('hidden');
        $('#cardImageContent').removeClass('hidden');
        updateCard();
        updateMiniPreviews();
        $('#imageForm')[0].reset();
    }
}

function updateCard(){
    var txt = $('#cardTextContent').val();
    var img = $('#cardImageContent').attr('src')

    var cardId = $('#cardPreview').attr('data-cardId');

    var miniPreview = $('.cardMiniPreview[data-cardId="' + cardId + '"]');
    miniPreview.find('label').text(txt);

    if (editingSide == 0){
        $('#frontText-' + cardId).val(txt);
        $('#frontImg-' + cardId).val(img);
    }
    else{
        $('#backText-' + cardId).val(txt);
        $('#backImg-' + cardId).val(img);
    }
}

function updateTheme(theme, shortName){
    var bigName = theme.replace('Small', '');
    var tinyName = theme.replace('Small', 'Mini');

    $('#themeField').val(shortName);
    theme = theme.replace(' ', '%20');
    $('#cardPreview').css('background-image', 'url(' + bigName +')');
    $('.cardMiniPreview').css('background-image', 'url(' + tinyName +')');
}

function updateCardList(){
    var newCardList = []

    $('.cardMiniPreview').each(function() {
        newCardList[newCardList.length] = $(this).attr('data-cardId');
    });

    $(cardIdList).val(newCardList.toString());

    var visibleCount = $('.cardMiniPreview:not(.cardRemoved)').length;

    $('#cardsContainer').css('width', (80*visibleCount) + 'px')

    $('#removeCard').toggle(visibleCount > 1);
}

function selectCard(card){
        var cardId = $(card).attr('data-cardId');

        if (editingSide == 0)
        {
            $('#cardTextContent').val($('#frontText-' + cardId).val());
            $('#cardImageContent').attr('src', $('#frontImg-' + cardId).val())
        }
        else{
            $('#cardTextContent').val($('#backText-' + cardId).val());
            $('#cardImageContent').attr('src', $('#backImg-' + cardId).val())
        }

        if ($('#cardImageContent').attr('src') != '')
        {
            $('#cardTextContent').addClass('hidden');
            $('#cardImageContent').removeClass('hidden');
        }
        else
        {
            $('#cardImageContent').addClass('hidden');
            $('#cardTextContent').removeClass('hidden');
        }


        $('#cardPreview').attr('data-cardId', cardId);
        $('.cardMiniPreview').removeClass('cardSelected');
        $(card).addClass('cardSelected');
}

function previewUploadedImage() {
    if( navigator.sayswho= (function(){
            var ua= navigator.userAgent, tem,
            M= ua.match(/(opera|chrome|safari|firefox|msie|trident(?=\/))\/?\s*(\d+)/i) || [];
            if(/trident/i.test(M[1])){
                tem=  /\brv[ :]+(\d+)/g.exec(ua) || [];
                return 'IE '+(tem[1] || '');
            }
            if(M[1]=== 'Chrome'){
                tem= ua.match(/\bOPR\/(\d+)/)
                if(tem!= null) return 'Opera '+tem[1];
            }
            M= M[2]? [M[1], M[2]]: [navigator.appName, navigator.appVersion, '-?'];
            if((tem= ua.match(/version\/(\d+)/i))!= null) M.splice(1, 1, tem[1]);
            return M.join(' ');
    })().indexOf("IE") >= 0) {
        $("#noPreview").slideDown();
        return;
    } /*else {
        console.log(
            navigator.sayswho= (function(){
            var ua= navigator.userAgent, tem,
            M= ua.match(/(opera|chrome|safari|firefox|msie|trident(?=\/))\/?\s*(\d+)/i) || [];
            if(/trident/i.test(M[1])){
                tem=  /\brv[ :]+(\d+)/g.exec(ua) || [];
                return 'IE '+(tem[1] || '');
            }
            if(M[1]=== 'Chrome'){
                tem= ua.match(/\bOPR\/(\d+)/)
                if(tem!= null) return 'Opera '+tem[1];
            }
            M= M[2]? [M[1], M[2]]: [navigator.appName, navigator.appVersion, '-?'];
            if((tem= ua.match(/version\/(\d+)/i))!= null) M.splice(1, 1, tem[1]);
            return M.join(' ');
            })()
        );
    }*/

    var input = $("#uploadImagesButton")[0];

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

function checkImgSize() {
    /* -> if the img selected is < 5MB */
    var img = $("#uploadImagesButton")[0].files[0];
    var mbytes = (img.size / (1024 * 1024)).toFixed(2);

    if( mbytes > 5 ) {
        alert("The image you are trying to upload is larger than our 5MB limit. " +
              "Your image is " + mbytes + "MB.\n\n" +
              "Try shrinking the image, then re-uploading it.");

        return false;
    }

    return true;
}

function checkImgType() {
    /* -> if the img selected is an acceptable type */
    var img = $("#uploadImagesButton")[0].files[0];
    var type = img.type;
    // console.log(type);
    if( type != "image/jpeg" && type != "image/png" &&
        type != "image/gif"  && type != "image/bmp") {
        alert("The type of file you are trying to upload is not supported or allowed. " +
              "Please only upload one of the following types of images:\n" +
              "- JPEG (.jpg or .jpeg)\n" +
              "- Portable Network Graphics (.png)\n" +
              "- Animated GIF (.gif)\n" +
              "- Bitmap (.bmp)");
        return false;
    }
    return true;
}

function validateImage() {
    try {
        var img = $("#uploadImagesButton")[0].files[0];
    } catch(err) {
        previewUploadedImage();
        var img = document.getElementById("uploadImagesButton").item(0);
        console.log("Img = ", img);
    }

    if( img == undefined )
        return false;


    var imgOK  = checkImgSize();
    var typeOK = checkImgType();
    if( !(imgOK && typeOK) ) {
        $("#imageForm").find("input[type=file]").val("");
        return false;
    }
    previewUploadedImage();
    return true;
}

function updateMiniPreviews()
{
    if (editingSide == 0)
    {
        $('.cardMiniPreview').each(function() {
            var cardId = $(this).attr('data-cardId');
            var thisTxt = $('#frontText-' + cardId).val();
            var thisImg = $('#frontImg-' + cardId).val();

            var lbl = $(this).find('label');
            var img = $(this).find('img');
            lbl.text(thisTxt);
            img.attr('src', thisImg);

            if (thisImg != '')
            {
                lbl.addClass('hidden');
                img.removeClass('hidden');
            }
            else
            {
                img.addClass('hidden');
                lbl.removeClass('hidden');
            }

        });
    }
    else{
        $('.cardMiniPreview').each(function() {
            var cardId = $(this).attr('data-cardId');
            var thisTxt = $('#backText-' + cardId).val();
            var thisImg = $('#backImg-' + cardId).val();

            var lbl = $(this).find('label');
            var img = $(this).find('img');
            lbl.text(thisTxt);
            img.attr('src', thisImg);

            if (thisImg != '')
            {
                lbl.addClass('hidden');
                img.removeClass('hidden');
            }
            else
            {
                img.addClass('hidden');
                lbl.removeClass('hidden');
            }

        });
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
        cardImage = cardImage.replace(new RegExp('"', 'g'), "'");
        var newPreviewDiv =  $('<div class="cardMiniPreview cardMiniPreview-add" data-cardId="' + cardId + '" style="background-image:' + cardImage + '" ></div>');
        var newLabel = $('<label></label>');
        var newImage = $('<img src="" class="hidden">');
        var newFrontField = $('<input  id="frontText-' + cardId  + '" type="hidden" name="front-' + cardId + '" value="">');
        var newFrontImgField = $('<input  id="frontImg-' + cardId  + '" type="hidden" name="front-img-' + cardId + '" value="">');
        var newBackField = $('<input  id="backText-' + cardId  + '" type="hidden" name="back-' + cardId + '" value="">');
        var newBackImgField = $('<input  id="backImg-' + cardId  + '" type="hidden" name="back-img-' + cardId + '" value="">');

        $('#cardsContainer').append($(newPreviewDiv))
        //$(newPreviewDiv).insertBefore($(this));
        $(newPreviewDiv).append(newLabel);
        $(newPreviewDiv).append(newImage);
        $(newPreviewDiv).append(newFrontField);
        $(newPreviewDiv).append(newFrontImgField);
        $(newPreviewDiv).append(newBackField);
        $(newPreviewDiv).append(newBackImgField);
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
        updateMiniPreviews();
        selectCard($('.cardSelected'));
    })

    $('#submitDeckChanges').click(function(){

    })

    $('#cardTextContent').change(updateCard);
    $('#cardTextContent').keyup(updateCard);

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
        $('#uploadedImage').attr('src', '');
        $("#imgPreviewContainer").hide();
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

    $('#clearImages').click(function(){
        $('#cardImageContent').attr('src', '')
        updateCard();
        selectCard($('.cardSelected'))
        updateMiniPreviews();

    });

    $("#uploadImagesButton").change( validateImage );
    $("#imageForm").attr("onsubmit", "validateImage()");
    $("#imageForm").submit( validateImage );

    $('#upload-target').on('load', img_upload_completed);

    $('#imageForm input:file').change(function(){
        $('#imageForm input:submit').removeClass('disabled');
    });

    $('#imageForm input:submit').click(function(){
        if (!$(this).hasClass('disabled'))
        {
            $("#overlay").hide();
            $("#imageDrawer").hide();
            $("#imgPreviewContainer").hide();

            $(this).addClass('disabled');
            $('#uploadedImage').attr('src', '');
            $('#submitUpload').addClass('disabled');
        }
    });

    selectCard($('.cardSelected'))

    updateCardList();
    updateMiniPreviews();
});
