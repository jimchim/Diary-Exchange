// this function is shared by new_entry and entry_edit, both uses the same code to start a summernote instance

var summernote = $('#summernote').summernote({
	height:400,
	focus: true,
	toolbar: [
		['style', ['bold', 'italic', 'underline', 'clear']],
		['fontsize', ['fontsize']],
		['color', ['color']],
		['para', ['ul', 'ol', 'paragraph']],
		['insert', ['picture', 'link']], // no insert buttons
		['help', ['help']] //no help button
		//['style', ['style']], // no style button
		//['height', ['height']],
		//['table', ['table']], // no table button
	],

	onChange: function(){
		var content = $('#summernote').code()
		$('textarea[name="body"]').val(content)
		resetTimer()
	},

	onImageUpload: function(files, editor, welEditable){
		if (!isAcceptedImageFile(files[0])) {
			showToastWarning('Image not accepted, please upload JPG/GIF/PNG/BMP images that are under 30MB.')				
			return
		}
		validateImage(files[0],function(imageFile, imageObject){
			sendPhoto(imageFile, function(result){
				editor.insertImage(welEditable,result)					
				resetTimer()					
			})
		})
	}
});	