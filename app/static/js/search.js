$(document).ready(function(){
  console.log("Hello");

  $( '#search-btn' ).click(function(){
    $('.results').remove()
    var searchObj = {}
    if ($('#search-color').val() != undefined) {
      searchObj.color = $('#search-color').val()
    }

    if ($('#search-price').val() != undefined) {
      searchObj.price = $('#search-price').val()
      searchObj.priceRange = $('#price-select').val()
    }

    if ($('#search-chair-select').val() != undefined) {
      searchObj.chair_count = $('#search-chair-select').val()
    }

    if ($('#search-length').val() != undefined) {
      searchObj.length = $('#search-length').val()
    }

    if ($('#search-width').val() != undefined) {
      searchObj.width = $('#search-width').val()
    }

    if ($('#search-height').val() != undefined) {
      searchObj.height = $('#search-height').val()
    }


    if ( searchObj.height || searchObj.width || searchObj.length) {
      searchObj.dimensionRange = $('#dimension-select').val()
    }
    console.log('search obj ', searchObj)
    $.ajax({
      type: 'POST',
      url: '/api-search',
      data: JSON.stringify(searchObj),
      dataType: 'json',
      contentType: 'application/json; charset=utf-8',
      success: function(response) {
          console.log(response);
          if (response.results.length > 0) {
            $.each(response.results, function(index, obj){
              if (!obj.photo) {
                obj.photo = 'app/static/img/yose.jpg'
              }
              var photo = obj.photo.slice(3)
              var html = '<div class="row results"><div class="col-xs-6">'
              html += '<h3>' + obj.name + " #" + obj.catalog_no + '</h3>'
              html += '<h5>' + obj.price + '</h5>'
              html += '<p>L: ' + obj.length + ' W: ' + obj.width + " H: " + obj.height + '</p>'
              html += '<p>Color: ' + obj.color + '</p>'
              html += '<p>Chairs: ' + obj.chair_count + ', color: ' + obj.chair_color + '</p>'

              html+= "</div>"
              html+= "<div class='col-xs-6'>"
              html+= '<img src="' + photo + '" alt="image not found" class="result-photo">'
              html+= "</div></div>"
              $('#search-results').append(html)

            })
          }
          else {
            var html = '<div class="results center"><h2>No results were found, try changing your search filters.</h2></div>'
            $('#search-results').append(html)
          }

      },
      error: function(error) {
          console.log(error);
      }
    });
  })
});
