"Use strict";

var body = document.querySelector('body');
var button = document.querySelector('.modal-btn');


//dim 생성 함수

var createDim = function() {
  var dim_layer = document.createElement('div');
  dim_layer.setAttribute('class', 'dim');
  body.appendChild(dim_layer);
  // 제거 이벤트 연결
  dim_layer.onclick = removeDimModal;
};



//modal-window 생성 함수

var createModalWindow = function(){
  var modal_window = document.createElement('div');
  modal_window.setAttribute('class', 'modal-window');
  return modal_window;
};

//modal-head 생성 함수

var createModalHead = function(){
  var modal_head = document.createElement('h3');
  modal_head.setAttribute('class', 'modal-head');
  var modal_head_text = document.createTextNode("What's NULL?");
  modal_head.appendChild(modal_head_text);
  return modal_head;
};

//modal-text 생성 함수

var createModalText = function(){
  var modal_text = document.createElement('p');
  modal_text.setAttribute('class', 'modal-text');
  var modal_text_p = document.createTextNode("NULL은 내 주변에서 같은 관심사를 가진 사람들을 묶어 주는 서비스입니다. 다양한 해시태그로 나와 맞는 사람들을 찾아보세요. 취미생활부터 최신 트렌드까지, 즐거운 이야기들이 당신을 기다립니다!");
  modal_text.appendChild(modal_text_p);
  return modal_text;
};

//modal-btn 생성 함수

var createModalBtn = function(){
  var modal_close_btn = document.createElement('button');
  modal_close_btn.setAttribute('type', 'button');
  modal_close_btn.setAttribute('aria-label', 'Close Modal');
  modal_close_btn.setAttribute('class', 'modal-close-btn');
  var modal_close_btn_text = document.createTextNode("닫기");
  modal_close_btn.appendChild(modal_close_btn_text);
  return modal_close_btn;
};


//합체!

function createModal(){
  var container = createModalWindow();
  var head = createModalHead();
  var text = createModalText();
  var close_btn = createModalBtn();
  container.appendChild(head);
  container.appendChild(text);
  container.appendChild(close_btn);
  body.appendChild(container);

  close_btn.onclick = removeDimModal;
}


//modal 제거 함수 생성

var removeDimModal = function(){
  var modal = document.querySelector('.modal-window');
  modal.parentNode.removeChild(modal);
  var dim = document.querySelector('.dim');
  dim.parentNode.removeChild(dim);
};


function createAllLayer() {
  createDim();
  createModal();
}



// 이벤트 걸기

button.onclick = createAllLayer;
