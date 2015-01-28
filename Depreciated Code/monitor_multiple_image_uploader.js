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


$('#multi').change(function(){

	// prevent user trying to submit multiple images 
	$('input[name="invalid-images"]').val(null) 
	fileList = []


	if (this.files.length < 1) {
		console.log('Empty file input at #multi')
		return
	}
	
	//else

	var files = this.files
	var invalidFiles = []
	var allowedFormat = ['jpg', 'jpeg', 'gif','png','bmp']				

	for (var i = 0; i < files.length ; i++) {										
		var file = this.files[i]
		var name = file.name
		var extension = file.name.split('.').pop().toLowerCase() // ensure match with lowercased allowedFormat
		var sizeInMB = file.size/1024/1024					

		if (sizeInMB > 50) { 
			invalidFiles.push(file) 
			console.log(name + ' is too big, please upload images under 50 MBs.')
		}

		if ( allowedFormat.indexOf(extension) == -1 ) {  // not in allowed formats
			invalidFiles.push(file) 
			console.log(name + ' is not in a supported file format, please upload JPG / GIF / PNG or BMP images only.')
		}

		try {
			verifyImage(file)
		}

		catch (error) {
			console.log('foo.jpg?')
		}					
		
	} // end for				
	return 
})		