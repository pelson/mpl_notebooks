$(document).ready(function() {

  // $(".notebook").each(function() {
  //   $(this).height(Math.random() * 300+250);
  // });

    var selected = [];

    $(".tag").click(function() {
        if($(this).hasClass("selected")){
            $(this).removeClass('selected');
        }
        else{
            $(this).addClass('selected');
        }
    });

    $("#clear").click(function() {
      selected = [];

      $(".tag").each(function(){
        tagOff($(this));
      });

    });

    function tagOff(tag){
      tag.removeClass('selected');
    }

});

$(window).load(function() {

  var nb = $(".notebooks");
  nb.masonry({
    // options
    itemSelector: '.notebook',
    isFitWidth: true
  });

});