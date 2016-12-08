$(document).ready(function(){

  $('.mypage-navi').find('a').click(function(){
    $('.page-div').hide();
    $('#'+$(this).attr('class')).show();

  });

});
