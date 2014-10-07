var carouselBaseHeight = 300;
var carouselBaseWidth = 805;

function nextSlide(){
    var _next = false;
    $('.button').each(function(){
        if(_next){
            $(this).addClass('active');
            _next = false;
        }
        else if($(this).hasClass('active')){
            _next = true;
            $(this).removeClass('active')
        }
    });
    if(_next)
        $(".button:eq(0)").addClass("active");

    var activeIndex = parseInt($(".active").attr("rel"));
    var slideWidth = $('#carousel').innerWidth();
   $('#carousel .slide').animate({left:-slideWidth*(parseInt(activeIndex)-1)});
}

function adjustCarouselSize()
{
    var maxWidth = $('#carousel').innerWidth();
    var scaleRatio = (maxWidth/carouselBaseWidth);
    var newHeight = carouselBaseHeight * scaleRatio;

    $('#carousel .slide').css('width', $('.image').length * carouselBaseWidth);
    $('#carousel').css('height', newHeight);

    $('.image').css('height', newHeight);
    $('.image').css('width', maxWidth);

    $('.image img').each(function(){
        var origWidth = $(this).attr('data-width');
        var newWidth = origWidth*scaleRatio;
        if (newWidth > origWidth) {
            newWIdth = origWidth;
        }
        $(this).css('width', newWidth);
    });

    activeIndex = $('.active').attr('rel');
    $('#carousel .slide').css('left', -(maxWidth*(parseInt(activeIndex)-1)));
}

function storeOriginalImageWidth()
{
    $('.image img').each(function(){
     $(this).attr('data-width', $(this).width())
    });

}

$(document).ready(function (){
    $('.button').click(function(){
        var slideWidth = $('#carousel').innerWidth();
        clearInterval(interval);
        var relatedId = $(this).attr('rel');
        $('#carousel .slide').animate({left: -slideWidth * (parseInt(relatedId) - 1)})
        $('.button').each(function(){
            $(this).removeClass('active');
            if($(this).attr('rel') == relatedId){
                $(this).addClass('active')}
        });
    });

    $(window).on('resize', adjustCarouselSize);

    storeOriginalImageWidth();
    adjustCarouselSize();
    interval = setInterval ( function(){ nextSlide(); }, 5000  );
});
