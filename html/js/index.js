$(document).ready(function() {

  // $(".notebook").each(function() {
  //   $(this).height(Math.random() * 300+250);
  // });

    var selected = [];

    $(".tag").click(function() {
        if($(this).hasClass("selected")){
            $(this).removeClass('selected');
            updateSelected();
        }
        else{
            $(this).addClass('selected');
            selected.push($(this).text());

        }
        console.log(selected);
    });

    $("#clear").click(function() {
      selected = [];

      $(".tag.selected").each(function(){
        tagOff($(this));
      });

    });

    function tagOff(tag){
      tag.removeClass('selected');
    }

    function updateSelected(){
      selected = [];
      $(".tag.selected").each(function() {
        selected.push($(this).text());
      });
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