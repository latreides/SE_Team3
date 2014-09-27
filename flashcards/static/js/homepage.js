jQuery(document).ready(function(){
	if( jQuery('#carouselNav li:first-child').is(':hidden') ) {
		jQuery('#carouselNav li:first-child').toggle();
	}
	var carouselInterval = 5000;
	function carouselSlide(){
		if( jQuery('#carouselNav li:visible').next().length == 0 ) {
			jQuery('#carouselNav li:last-child').slideUp('fast');
			jQuery('#carouselNav li:first-child').slideDown('fast');
		} else {
			jQuery('#carouselNav li:visible').slideUp('fast').next('li:hidden').slideDown('fast');
		}
	}
	var carouselScroll = setInterval(carouselSlide,carouselInterval);
	jQuery('#carousel').hover(function() {
		clearInterval(carouselScroll);
	}, function() {
		carouselScroll = setInterval(carouselSlide,carouselInterval);
		carouselSlide();
	});
});