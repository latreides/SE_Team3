var carouselInterval = 5000;
var carouselScroll;

function carouselInit()
{
    $('#carouselNav img:first-child').show();
    carouselScroll = setInterval(carouselSlide,carouselInterval);
}

function carouselSlide()
{
    if( $('#carouselNav img:visible').next().length == 0 )
    {
        $('#carouselNav img:last-child').slideUp('fast');
        $('#carouselNav img:first-child').slideDown('fast');
    }
    else
    {
        $('#carouselNav img:visible').slideUp('fast').next('img:hidden').slideDown('fast');
    }
}

$(document).ready(function(){
    $('#carousel').hover(function() {
        clearInterval(carouselScroll);
    }, function() {
        carouselScroll = setInterval(carouselSlide,carouselInterval);
        carouselSlide();
    });

    carouselInit();

});
