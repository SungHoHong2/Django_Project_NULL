$(document).ready(function(){


// 1. 글쓰기 클릭 시 modal 창 생성, 삭제

    var modal = document.getElementById('myModal');
    var btn = document.getElementById("myBtn");
    var span = document.getElementsByClassName("modal-close")[0];
    var dim = document.getElementsByClassName("dim")[0];

    var img_links = $(".visual-container").children('a');



    // 버튼 클릭 시 모달 창 띄우기 //
    btn.onclick = function() {
      modal.style.display = "block";
      dim.style.display = "block";
    }

    // X 클릭하면 모달 닫기 //
    span.onclick = function() {
      modal.style.display = "none";
      dim.style.display = "none";
    }


    // ?????????
    $('#post_btn').click(function(){

      // $('#id_hash_tags').val('')
      // $({{ hash_tags|safe }}).each(function(index, item){
      //
      //     var text = $('#hash_tag_ids').val();
      //     if(text.length>0){
      //       text+=','
      //     }
      //     text+=item.id;
      //     $('#hash_tag_ids').val(text);
      // });

      $('#myBtn').trigger('click');

    });


// 2. 채팅 버튼 클릭했을 시 페이지 이동
    $('#chat_btn').click(function(){
      location.href = "/saytalk/chat_detail/1/";
    });


// 3. 이미지 데이터를 가져와서 뷰 단에 붙이기
    // $("#photo_list_templ").tmpl({{ talk_list|safe }}).appendTo( "#photo_add_content" );


// ??????
    $('#file_temp_submit').click(function(){

        var form_data = new FormData();
        form_data.append("img_file",$('input[name=img_file]')[0].files[0])
        formAjax('POST', form_data, "{% url 'collection:temp_image' %}",
        'application/json', function(response){
                console.log(response);
                var text = $('#image_file_ids').val();

                if(text.length>0){
                  text+=','
                }

                text+=response.id
                $('#image_file_ids').val(text)
                $('#post_image_display').append($('<img/>').width(100).height(100).attr('src',response.img_file))
        })

    });


// 5. Detail 버튼 클릭 시
    $('.detail_btn').click(function(){
        location.href = '/saytalk/talk_detail/'+$(this).attr('id');
    });




// 6. a 클릭하면 이미지 hover 효과

  for ( var i=0, l=img_links.length; i<l; i++ ){
    var img_link = img_links[i];

    img_link.onclick = makeHover;
}

function makeHover(){
    if ($(this).hasClass('hover')) {
        $(this).removeClass('hover');
    }
    else {
      $(this).addClass('hover');
    }
  };


});


// 이미지 자동 정렬
// $(function(){
//   var vg = $("#photo_add_content").vgrid({
//     easing: "easeOutQuint",
//     useLoadImageEvent: true,
//     time: 1000,
//     delay: 20,
//     fadeIn: {
//       time: 1000,
//       delay: 100,
//       wait: 1000
//     }
//   });
//   $(window).load(function(e){
//     vg.vgrefresh();
//   });
// });
