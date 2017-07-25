$(document).ready(function(){

  $( '#admin-delete-btn' ).click(function(){
    var searchObj = {catalog_no: $('#edit-item').val()}

    if (!searchObj.catalog_no) {
      alert("Please enter a catalog number before deleting.")
      return
    }

    $.ajax({
      type: 'POST',
      url: 'admin/api-delete',
      data: JSON.stringify(searchObj),
      dataType: 'json',
      contentType: 'application/json; charset=utf-8',
      success: function(response) {
          console.log(response);
          $('#messages').show()

      },
      error: function(error) {
          console.log(error);
      }
    });
  })
})
