(function($){
    $.fn.displaydecks = function(){
        return this.each(function(){
            obj = $(this)
            obj.find('.button').click(function() {
                obj.find('.menu').fadeIn(400);
                
                obj.find('.menu').hover(function(){ },
                    function(){
                        $(this).fadeOut(400);
                    }
                );
            });
            
            obj.find('.menu li').click(function() {
            obj.find('.button')
                
                
            obj.find('.menu').fadeOut(400);
            });
        });
    };
})(jQuery);
        
$(function(){
    $('.switch').displaydecks();
});