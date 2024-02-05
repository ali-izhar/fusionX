function previewImage(event, imgId) {
    var reader = new FileReader();
    reader.onload = function(){
        var output = document.getElementById(imgId);
        output.src = reader.result;
    };
    reader.readAsDataURL(event.target.files[0]);
}