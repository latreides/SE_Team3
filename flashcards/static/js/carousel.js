$(document).ready(function (){

    $('#button a').click(function(){
        clearInterval(interval);
        var integer = $(this).attr('rel');
        $('#carousel .slide').animate({left:-705*(parseInt(integer)-1)})
        $('#button a').each(function(){
            $(this).removeClass('active');
            if($(this).hasClass('button'+integer)){
                $(this).addClass('active')}
        });
    });
        Next();
        interval = setInterval ( function(){Next();}, 5000 );
    });
    
    function Next(){
        var _next = false;
        $('#button a').each(function(){
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
            $("#button a:eq(0)").addClass("active");
        
       var activeIndex = parseInt($(".active").attr("rel"));
       $('#carousel .slide').animate({left:-705*(parseInt(activeIndex)-1)});      
    }

