var scope = {}

$(document).ready(function(){
  console.log("app/static/img/".length)
  $( '#admin-edit-search-btn' ).click(function(){
    $('#messages').hide()
    var searchObj = {catalog_no: $('#edit-item').val()}

    if (!searchObj.catalog_no) {
      alert("Please enter a catalog number before searching.")
      return
    }

    $.ajax({
      type: 'POST',
      url: '/api-search',
      data: JSON.stringify(searchObj),
      dataType: 'json',
      contentType: 'application/json; charset=utf-8',
      success: function(response) {
          console.log(response);
          if (response.results.length > 0) {
            scope.editId = response.results[0]._id

            console.log("editId", scope)
            $.each(response.results, function(index, obj){
              if (!obj.photo) {
                obj.photo = 'app/static/img/yose.jpg'
                scope.editPhoto = obj.photo.slice(15)
              }
              else {
                scope.editPhoto = obj.photo.slice(19)
              }

              var photo = obj.photo.slice(3)


              $('#edit-image').attr('src', photo)
              $('#edit-image').show()

              function populateForm(form, data) {
                console.log("data", data)
                $.each(data, function(key, value){
                  console.log("key ", key)
                  if (key != 'image' || key != 'photo' || key != 'file' || key != 'imageName') {
                    $('[name=' + key + ']', form).val(value)
                  }
                })
              }

              populateForm($('#edit-form'), obj)


            })
          }
          else {
            var html = '<div class="results center"><h2>No results were found.</h2></div>'
            $('#edit-section').append(html)
          }

      },
      error: function(error) {
          console.log(error);
      }
    });

  })

  $( '#edit-now-btn' ).click(function(ev){
    console.log('clicked')
    ev.preventDefault()
    var editItem = {} //json of form inputs, name: value
    var formObj = new FormData()
    editItem.id = scope.editId

    $('#edit-form :input').each(function(){
      if ($(this).attr('name') && $(this).attr('name').length > 0 && $(this).attr('name') != 'csrf_token' && $(this).attr('name') != 'new-image') {
        editItem[$(this).attr('name')] = $(this).val()
      }
      if ($(this).attr('name') === 'new-image' && $(this).val().length > 0) {
        console.log('firing')
        //editItem.imageName = $(this).val()
        editItem.photoToRemove = scope.editPhoto

        formObj.append('image', $('input[type=file]')[0].files[0]);
      }
    })


    if (!editItem.photoToRemove) {
      editItem.photoToRemove = 'None'
    }
    console.log(editItem)
    formObj.append("newData", JSON.stringify(editItem))
    //editItem.formData = formData



    $.ajax({
      type: 'POST',
      url: 'admin/api-edit',
      data: formObj,
      dataType: 'json',
      contentType: false,
      processData: false,
      // async: false,
      cache: false,
      success: function(response) {
          console.log(response);


      },
      error: function(error) {
          console.log(error);
      }
    });
  })
});
