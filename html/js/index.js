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
            selected.push($(this).text().toLowerCase());

        }
        console.log(selected);

        updateTags();
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
        selected.push($(this).text().toLowerCase());
      });
    }


    function arraysOverlap(a, b){
      for (var i = 0; i < a.length; i++) {
        for (var j = 0; j < b.length; j++) {
          if(a[i] === b[j]){
            return true;
          }
        }
      }
      return false;
    }

    function updateTags(){
      $(".notebooks").each(function() {
        var wrapper = $(this);
        $(".notebook").each(function() {
          var nb = $(this);
          var nbtags = nb.data("keywords");

          var visible = true;

          for (var i = 0; i < selected.length; i++) {
            var sel = selected[i];
            var nbHasTag = false;
            for (var j = 0; j < nbtags.length; j++) {
              if(sel === nbtags[j]){
                nbHasTag = true;
              }
            }
            if(!nbHasTag){
              visible = false;
              i = selected.length;
            }
          }

          if(selected.length === 0 || visible){
            nb.removeClass("hide");
            wrapper.masonry('layout');
          }
          else if(!visible){
            nb.addClass("hide");
            wrapper.masonry('layout');

          }
        });
        if(wrapper.children(":not(.hide)").length === 0){
          // console.log("nothing");
          wrapper.prev().hide();
        }
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