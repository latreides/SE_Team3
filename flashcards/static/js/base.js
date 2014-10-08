function recalcHeaderSize()
{
    $('#nav-header').toggleClass('wide-header', $(this).width() >= 900)
    $('#nav-header').toggleClass('narrow-header', ($(this).width() < 900) && ($(this).width() > 500))
    $('#nav-header').toggleClass('sqeeze-header', $(this).width() <= 400)

}

$(document).ready(function()
{
    $(window).on('resize', recalcHeaderSize);

    // Because a resize is not (always) raised when the document loads
    recalcHeaderSize();
});
