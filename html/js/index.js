$(document).ready(function() {
    var container = document.querySelector('.notebooks');
    var msnry = new Masonry( container, {
      // options
      itemSelector: '.notebook',
      isFitWidth: true
    });
});