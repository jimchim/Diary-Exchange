$('#image-uploader').change(function(){
	if (this.files.length < 1) {
		return
	};
	for (var i = 0; i < this.files.length ; i++) {										
		var file = this.files[i]
		if (isValidImageFile(file)) {
			console.log(file.name + " is valid image");
			try {
				validateImage(file, function(imageFile, imageObject){
					appendImage($('#image-previews'), imageObject.src)												
				});
			}
			catch (error) {
				console.log('Image Validation Failed');
			}				
		}						
		else {
			console.log(file.name + " is not valid image");
		}
	} // end for				
})
