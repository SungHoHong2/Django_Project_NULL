

//이미지 자동 정렬
$(function(){
  var vg = $("#photo_add_content").vgrid({
    easing: "easeOutQuint",
    useLoadImageEvent: true,
    time: 1000,
    delay: 20,
    fadeIn: {
      time: 1000,
      delay: 100,
      wait: 1000
    }
  });
  $(window).load(function(e){
    vg.vgrefresh();
  });
});
