window.onload = function () {

  window.requestAnimFrame = (function(){
          return  window.requestAnimationFrame   ||
              window.webkitRequestAnimationFrame ||
              window.mozRequestAnimationFrame    ||
              function( callback ){
                  window.setTimeout(callback, 1000 / 60);
              };
      })();


  window.clearAnimation = (function() {
        return window.cancelRequestAnimationFrame ||
          window.cancelAnimationFrame ||
          window.mozCancelRequestAnimationFrame ||
          window.oCancelRequestAnimationFrame ||
          window.msCancelRequestAnimationFrame ||
            function(id){
                clearTimeout(id)
            };
    })();


  var slider = document.querySelector('.slider');
  var slider_lis = slider.querySelectorAll('li');

  var slide_count = slider.childElementCount;
  var slide_width = slider.children[0].clientWidth;
  var slider_width = slide_count*slide_width;
  var offset = 0;
  var y = slide_width;
  var sliding;

  for ( var i=0; i<slide_count; i++ ){
    var slider_li = slider_lis[i];
    // slider_li.style.width = slider_li_width  + 'px';
    // slider_lis[i].className = "slide-" + (i+1);
  }

    slider.style.width = slider_width + 'px';


  var navi = document.querySelector('.navigation');
  var links = navi.querySelectorAll('a');

  for ( var n=0; n<slide_count; n++ ){
    var link = links[n];
    links[n].className = "link" + (n+1);
    linkIndex = (n+1);
  }

  function linkClick(){
    if(offset<linkIndex*slide_width){
      offset+=64;
      slider.style.left = -offset+"px";
      if(offset==linkIndex*slide_width){
          clearAnimation(sliding);
          y=slide_width*linkIndex+slide_width;
        }
    }
    else if(offset>linkIndex*slide_width){
      offset-=64;
      slider.style.left = -offset+"px";
      if(offset==linkIndex*slide_width){
          clearAnimation(sliding);
          y=slide_width*linkIndex+slide_width;
        }
    }
    else {
      clearAnimation(sliding);
      return false;
    }
}

function btnClick(){
  offset+=64;
  slider.style.left = -offset+"px";
  if(offset==1*slide_width){
      clearAnimation(sliding);
    }
}

var link_btn = document.querySelector('.link-btn');

  for (var i=0; i<slide_count; i++){
    (function(index){
      links[i].onclick = function(){
        linkIndex = index;
        (function animloop(){
          sliding = requestAnimFrame(animloop);
          linkClick();
        })();
        return false;
      };
      link_btn.onclick = function(){
        (function animloop(){
          sliding = requestAnimFrame(animloop);
          btnClick();
        })();
        return false;
      };
    })(i);
  }


};
