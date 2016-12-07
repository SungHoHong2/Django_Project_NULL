$(document).ready(function(){
  //
  // var pf_links = $('.mypage-navi').find('a');
  //
  // for ( var i=0, l=pf_links.length; i<l; i++ ){
  //   var pf_link = pf_links[i];
  //
  //   pf_link.onclick = showPages;
  // }
  //
  // function showPages(){
  //   var link_class = $(this).attr('class');
  //   var page = $('.mypage-view').children("'." + link_class + "'");
  //   // $(page).hide();
  // };
  //
  //
  //


  $('#my-profile').click(function(){
    $('.my-profile').show();
    $('.my-post').hide();
    $('.my-chat').hide();
    $('.my-like').hide();
    $('.my-version').hide();
  });

  $('#my-post').click(function(){
    $('.my-profile').hide();
    $('.my-post').show();
    $('.my-chat').hide();
    $('.my-like').hide();
    $('.my-version').hide();
  });

  $('#my-chat').click(function(){
    $('.my-profile').hide();
    $('.my-post').hide();
    $('.my-chat').show();
    $('.my-like').hide();
    $('.my-version').hide();
  });

  $('#my-like').click(function(){
    $('.my-profile').hide();
    $('.my-post').hide();
    $('.my-chat').hide();
    $('.my-like').show();
    $('.my-version').hide();
  });

  $('#my-version').click(function(){
    $('.my-profile').hide();
    $('.my-post').hide();
    $('.my-chat').hide();
    $('.my-like').hide();
    $('.my-version').show();
  });



});
