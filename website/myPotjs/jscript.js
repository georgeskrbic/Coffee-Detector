
$(document).ready(function () {
  	$(function() {
  		var offset = 220;
  		var duration = 800;
  		jQuery(window).scroll(function() {
  			if (jQuery(this).scrollTop() > offset + 570) {
  				jQuery('.back-to-top').fadeIn(duration);
  			} else {
  				jQuery('.back-to-top').fadeOut(duration);
  			}
  		});

  		jQuery('.back-to-top').click(function(event) {
  			event.preventDefault();
  			jQuery('html, body').animate({scrollTop: 0}, duration);
  			return false;
  		})
  	});
	if ( $(window).width() > 800) {      
	  	//Add your javascript for large screens here 
	  	$( ".mobile" ).remove();
		var s = skrollr.init({
	    	smoothScrollingDuration: 2200
		});
	} 
	else {
  	//Add your javascript for small screens here
		$( ".bean" ).remove(); 
		$( ".desktop" ).remove(); 
	}

	//Upper page fade ins
	$('div.fadeIn').fadeIn(1000).removeClass('fadeIn');
	$('ul.fadeIn').fadeIn(800).removeClass('fadeIn');
	$('button.fadeIn').fadeIn(1400).removeClass('fadeIn');

	//scrolling fade ins
	//check every time scrolled
    $(window).scroll(function(){

    	/* Check the location of each desired element */
    	$('.fadeUp').each(function(i){

    		var bottom_of_object = $(this).offset().top + $(this).height();
    		var bottom_of_window = $(window).scrollTop() + $(window).height();

    		/* If the object is completely visible in the window, fade it in */
    		if(bottom_of_window > bottom_of_object){
    			if ( $(window).width() > 800) {      
					//Add your javascript for large screens here 
    				$(this)
    				.animate({'opacity':'1'}, 1000);
				} 
				else {
					//Add your javascript for small screens here
					$(this)
    				.animate({left:$(window).width() / 3.75, opacity:"show"}, 1000); 
				}
    		}

    	}); 
	  //   	$(function(){
			//     $('.bar1').hover(
			//         function(){
			//            $(this).animate({width: '100%'});
			//         }
			//     );                             
			// });
	    	    	/* Check the location of each desired element */
    	$('.bar1').each(function(i){

    		var bottom_of_object = $('.bar3').offset().top + $('.bar3').height() + 100;
    		var bottom_of_window = $(window).scrollTop() + $(window).height();

    		/* If the object is completely visible in the window, fade it in */
    		if(bottom_of_window > bottom_of_object){
    			if ( $(window).width() > 800) {      
					//Add your javascript for large screens here 
    				$(this)
    				.animate({'width':'100%'}, 2000);
    				$('.bar2')
    				.animate({'width':'50%'}, 1200);
    				$('.bar3')
    				.animate({'width':'0%'}, 1200);
				} 
				else {
					//Add your javascript for small screens here
					$(this)
    				.animate({left:$(window).width() / 3.75, opacity:"show"}, 1000); 
				}
    		}

    	}); 
    });

    //scrolling fade in/out
    $(window).on("load",function() {
    	//get bottom of welcome div
    	var $el = $('#welcome');  //record the elem so you don't crawl the DOM everytime  
		var bottom = $el.position().top + $el.outerHeight(true) + 100;
	  $(window).scroll(function() {
	    $(".fade").each(function() {
	      /* Check the location of each desired element */
	      var objectBottom = $(this).offset().top + $(this).outerHeight();
	      
	      if (objectBottom > bottom) { //object comes into view (scrolling down)
	        if ($(this).css("opacity")==0) {$(this).fadeTo(500,1);}
	      } else { //object goes out of view (scrolling up)
	        if ($(this).css("opacity")==1) {$(this).fadeTo(500,0);}
	      }
	    });
	  }); $(window).scroll(); //invoke scroll-handler on page-load
	});

});

