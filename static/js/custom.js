$(document).ready(function (e) {
    $( window ).on( "load", function() {
        $(".sidebar").mCustomScrollbar({
        	scrollInertia: 100
        });
    });
    $(".desc_option input[type='radio']").click(function(e){
    	 $(".desc_option_list").removeClass("active");
		 $(this).parents(".desc_option_list").addClass("active");
	});
	$(".tab_list").click(function(e){
    		e.preventDefault();
    		var thisHref = $(this).attr("href");
    		$(".menu li").removeClass("active");
    		$(this).parents("li").addClass("active");
    		$(".tab_info").removeClass("active");
    		$(thisHref).addClass("active");
	});
    if ($(window).scrollTop() >= 1) {
        if($(window).width() > 0){
            $('.header_admin').addClass('active');
        }
        else{
            $('.header_admin').removeClass('active');
        }
    }
     
    $(window).scroll(function () {
       var scroll = $(window).scrollTop();
       if (scroll >= 1) {
            $('.header_admin').addClass('active');
        }
        else {
            $('.header_admin').removeClass('active');
        }
    });
    $(".toggle_menu").click(function(e){
        $(".sidebar,body").toggleClass("active");
    });
    $(".video_overlay a").click(function(e){
        var videoSrc = $(this).attr("data-src");
        $(".model_video iframe").attr("src",videoSrc+"?autoplay=1");
    });
    $(".close").click(function(e){
        $(".model_video iframe").attr("src"," ");
    });
    $(".user_notification a").click(function(e){
        e.preventDefault();
        $(this).parents(".user_notification").find(".drop_down").slideToggle();
    });
    var currentCode = 1;
    $("#addoption").click(function(e){
        currentCode++;
        var character = String.fromCharCode(64 + currentCode);
        $(".add_option_list ul").append('<li>\
            <div class="group_outer d-flex flex-wrap">\
                <label>Option '+character+':</label>\
                <input type="text" class="form-control" name="">\
            </div>\
        </li>');
        $(".add_deci_list ul").append('<li><textarea class="form-control" placeholder="Decision Notification '+character+':"></textarea></li>');
        $(".deci_matrix_table tbody").append('<tr>\
                                            <td>Option '+character+'</td>\
                                            <td class="color-black">+19</td>\
                                            <td class="color-black">0</td>\
                                            <td class="color-black">-5</td>\
                                        </tr>');
    });
    $(document).mouseup(function(e) 
    {
        var container = $(".drop_down,.modal");
        if (!container.is(e.target) && container.has(e.target).length === 0) 
        {
            container.slideUp();
        }
    });
});