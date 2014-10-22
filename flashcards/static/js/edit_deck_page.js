
var newCardCounter = 0;
function updateText()
{
    var txt = $('#cardTextContent').val();
    var cardId = $('#cardPreview').attr('data-cardId');

    var miniPreview = $('.cardMiniPreview[data-cardId="' + cardId + '"]');
    miniPreview.text(txt)
    miniPreview.attr('data-text', txt)
}

function updateTheme(theme)
{
    theme = theme.replace(' ', '%20')
    $('#cardPreview').css('background-image', 'url(' + theme +')')
    $('.cardMiniPreview').css('background-image', 'url(' + theme +')')
}

$(document).ready(function(){
    $('#previewContainer').on("click", ".cardMiniPreview", function(){
        $('#cardTextContent').val($(this).attr('data-text-front'))
        $('#cardPreview').attr('data-cardId', $(this).attr('data-cardId'));

        $('.cardMiniPreview').removeClass('cardSelected');
        $(this).addClass('cardSelected');

      });

    $('.themePreview').click(function(){
        $('.themePreview').removeClass('themeSelected');
        $(this).addClass('themeSelected');
        updateTheme($(this).attr('src'));
    });

    $('#addCard').click(function(){
        var cardImage = $('.cardSelected').css('background-image');
        $('<div class="cardMiniPreview" data-text="" data-cardId="new_'+ (newCardCounter++) +'" style="background-image:' + cardImage + '" ></div>').insertBefore($(this));

    });

    $('#cardTextContent').change(updateText);
    $('#cardTextContent').keyup(updateText);
});
