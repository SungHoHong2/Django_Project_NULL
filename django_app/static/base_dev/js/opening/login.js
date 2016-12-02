$(document).ready(function(){
        $('.login-btn').click(function(){

            var form_data = $("#login_form").serialize();
            $.ajax( {
                  type: "POST",
                  url:  "{% url 'member:login' %}",
                  data: form_data,
                  success: function( response ) {
                    location.reload();
                  },
                  error : function(response){
                        alert('아이디나 암호가 잘못되었습니다.');
                  }
            });

        });
});