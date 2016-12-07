$(document).ready(function(){
    // console.log({{ talk_detail|safe }})
        //  $("#saytalk_detail_templ").tmpl({{ talk_detail|safe }}).appendTo( "#post_detail_div" );
        //  $("#saytalk_comment_templ").tmpl({{ talk_detail|safe }}).appendTo( "#post_detail_div" );


// 댓글달기 modal 창

  var comment_modal = document.getElementById('mycomment');
  var comment_btn = document.getElementById("comment_btn");
  var span = document.getElementsByClassName("modal-close")[0];
  var dim = document.getElementsByClassName("dim")[0];


  // 버튼 클릭 시 모달 창 띄우기 //
  comment_btn.onclick = function() {
    comment_modal.style.display = "block";
    dim.style.display = "block";
  }

  // X 클릭하면 모달 닫기 //
  span.onclick = function() {
    comment_modal.style.display = "none";
    dim.style.display = "none";
  }


});
