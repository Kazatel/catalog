$(document).ready(function() {

  $.ajax({
    type: 'GET',
    url: '/api/genres',
    success: function(response) {
      var data = response.Genres;
      var menu =''
      for (var i = 0, len = data.length; i < len; i++) {
          menu = menu + '<a href="/genre/' + data[i].id + '/">' +
            '<div class="row">' +
              '<div class="col-md-1"></div>' +
              '<div class="col-md-10 genre-list">' +
              '<h3>' + data[i].name + '</h3>' +
              '</div>' +
              '<div class="col-md-1"></div>' +
            '</div></a>'
      }
      $('#Genre_menu').empty()
      $('#Genre_menu').append(menu)
    }
  });


/*
$('#new-game').unbind( "click" );
$('#new-game').bind( "click", function() {
  $.ajax({
    type: 'GET',
    url: '/api/genres',
    success: function(response) {
      var data = response.Genres;
      var select ='<option value="select">Select genre</option>';
      for (var i = 0, len = data.length; i < len; i++) {
          select = select + '<option value="'+ data[i].id + '">' + data[i].name +'</option>';
      }
      $('#genre_select').empty()
      $('#genre_select').append(select)
    }
});
});
*/

});
