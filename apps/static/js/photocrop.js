$(function () {

  /* SCRIPT TO OPEN THE MODAL WITH THE PREVIEW */
  $("#id_fileToCrop").change(function (e) {
    if (this.files && this.files.length>1) {
      var form=$("#id_fileToCrop").closest("form");
      form.submit();
    }
    else if (this.files && this.files[0]) {
      var form=$("#id_fileToCrop").closest("form");
      var path=this.files[0].name;
      var allowedExtensions = /(\.jpg|\.jpeg|\.png|\.gif)$/i;
      if(!allowedExtensions.exec(path.toLowerCase())){
          path = 'fileerror';
          $("#id_photo_fileSave").attr("value", "False");
          form.submit();
          return false;
        }
        else {
          var reader = new FileReader();
          reader.onload = function (e) {
            $("#id_cropImage").attr("src", e.target.result);
            $("#id_modalCrop").modal("show");
          }
          reader.readAsDataURL(this.files[0]);
        }
    }
  });
  /* SCRIPTS TO HANDLE THE CROPPER BOX */
  var $image = $("#id_cropImage");
  var cropBoxData;
  var canvasData;
  $("#id_modalCrop").on("shown.bs.modal", function () {
    $image.cropper({
      viewMode: 3,
      aspectRatio: 1/1,
      minCropBoxWidth: 50,
      minCropBoxHeight: 50,

      ready: function () {
        $image.cropper("setCanvasData", canvasData);
        $image.cropper("setCropBoxData", cropBoxData);
      }
    });
  }).on("hidden.bs.modal", function () {
    cropBoxData = $image.cropper("getCropBoxData");
    canvasData = $image.cropper("getCanvasData");
    $image.cropper("destroy");
  });

  $(".js-zoom-in").click(function () {
    $image.cropper("zoom", 0.1);
  });

  $(".js-zoom-out").click(function () {
    $image.cropper("zoom", -0.1);
  });


  /* SCRIPT TO COLLECT THE DATA AND POST TO THE SERVER */
  $(".js-crop-and-upload").click(function () {
    var cropData = $image.cropper("getData");
    $("#id_x").val(cropData["x"]);
    $("#id_y").val(cropData["y"]);
    $("#id_height").val(cropData["height"]);
    $("#id_width").val(cropData["width"]);
    var form=$("#id_fileToCrop").closest("form");
    $("#id_photo_fileSave").attr("value", "True");
    form.submit();
  });


});
