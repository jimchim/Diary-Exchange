/*var editor = new MediumEditor('.editor')*/
/*$('textarea[name="new-body"]').hide();*/
$(document).ready(function(){			


	$('#test').click(function(){
		var content = $('#summernote').code()
		$('textarea[name="new-body"]').val(content)
	})

	var summernote = $('#summernote').summernote({
		height:400,
		focus: true,
		toolbar: [
			//['style', ['style']], // no style button
			['style', ['bold', 'italic', 'underline', 'clear']],
			['fontsize', ['fontsize']],
			['color', ['color']],
			['para', ['ul', 'ol', 'paragraph']],
			//['height', ['height']],
			['insert', ['picture', 'link']], // no insert buttons
			//['table', ['table']], // no table button
			['help', ['help']] //no help button
		],
		onkeydown: function(){
			var content = $('#summernote').code()
			$('textarea[name="new-body"]').val(content)		
		},
		onImageUpload: function(files, editor, welEditable){
			console.log('image upload:', files[0])
			console.log('editor', editor)					
			verifyImage(files[0],function(e){
				editor.insertImage(welEditable,e)				
			})
		}
	});
	
	$('#edit-entry-form textarea').focus(function(){
		$(this).autosize();
	})

	$('input[type="submit"]').click(function(e){
		var sub = $('input[name = "new-subject"]').val()
		var bod = $('textarea[name = "new-body"]').val()								
		if (sub.length * bod.length == 0) {
			e.preventDefault()					
		}
	})

	

	var fileList = []

	function verifyImage(image, callback) {
		var reader = new FileReader()
		var img = new Image() // Image object used to test the uploaded image file

		reader.readAsDataURL(image)

		reader.onloadend = function(){
			img.src = reader.result
			img.onload = function(_image){
				var preview = document.getElementById('image-previews')						
				$(preview).append('<img src = "' + reader.result + '">')				
				callback(img.src)
				/*console.log(img.src)
				console.log(image)						*/
			}
			img.onerror = function(){
				console.log(image.name + ' is invalid')
				fileList.push(image.name)
				$('input[name="invalid-images"]').val(fileList)
			}					
		} 

		//console.log(image + ' is valid.')
	} 

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
			/*if () {
			}			*/
				/*invalidFiles.push(file)
				console.log(verified)			*/
			
		} // end for				
		return 
	})

})		