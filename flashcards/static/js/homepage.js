var carouselInterval = 5000;

function carouselInit()
{
    $('#carouselNav li:first-child').show();
    var carouselScroll = setInterval(carouselSlide,carouselInterval);
}

function carouselSlide()
{
    if( $('#carouselNav li:visible').next().length == 0 )
    {
        $('#carouselNav li:last-child').slideUp('fast');
        $('#carouselNav li:first-child').slideDown('fast');
    }
    else
    {
        $('#carouselNav li:visible').slideUp('fast').next('li:hidden').slideDown('fast');
    }
}

$(document).ready(function(){
    $('#carousel').hover(function() {
        clearInterval(carouselScroll);
    }, function() {
        carouselScroll = setInterval(carouselSlide,carouselInterval);
        carouselSlide();
    });
});
