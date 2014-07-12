$(document).ready(function() {

  // $(".notebook").each(function() {
  //   $(this).height(Math.random() * 300+250);
  // });

    $(".tag").click(function() {
        if($(this).hasClass("selected")){
            $(this).removeClass('selected');
        }
        else{
            $(this).addClass('selected');
        }
    });



});

$(window).load(function() {
  
    var container = document.querySelector('.notebooks');
    var msnry = new Masonry( container, {
      // options
      itemSelector: '.notebook',
      isFitWidth: true
    });

});