// this function is shared by new_entry and entry_edit, both uses the same code to start a summernote instance

currentEntry = false // two ajax call in this page may create an entry, need this variable to help determine if new entry should be created

var subject = $('input[name="subject"]')
var body = $('textarea[name="body"]')
var ID = $('input[name="entry-id"]')

var summernote = $('#summernote').summernote({
	height:400,	
	toolbar: [
		['style', ['bold', 'italic', 'underline', 'clear']],
		['fontsize', ['fontsize']],
		['color', ['color']],
		['para', ['ul', 'ol', 'paragraph']],
		['insert', ['picture', 'link']], // no insert buttons
		['help', ['help']] //no help button			
	],

	onChange: function(){				
		summernoteOnChange()
	},

	onImageUpload: function(files, editor, welEditable){
		summernoteOnImageUpload(files, editor, welEditable)		
	}
});

var summernoteOnChange = function(){	
	$(body).val(summernote.code())
	resetTimer()
}

var summernoteOnImageUpload = function(files, editor, welEditable){
	if (!isAcceptedImageFile(files[0])) {
		showToastWarning('Image not accepted, please upload JPG/GIF/PNG/BMP images that are under 30MB.')				
		return
	}

	var saveAndInsertPhoto = function(){
		validateImage(files[0],function(imageFile, imageObject){ //callback from validateImage()
			sendPhoto(imageFile, function(result){
				editor.insertImage(welEditable,result)					
				resetTimer()					
			})
		}
	)}

	if (currentEntry == false) {// if entry is not created, create one first.		
		saveEntry(function(){
			saveAndInsertPhoto()
		})												
	}
	else {
		saveAndInsertPhoto()
	}

}

$('textarea[name="body"]').hide();	//if summernote cannot instantiate, allow user to use textarea

var saveEntry = function(callback){		
	var formData = new FormData()
	formData.append('csrfmiddlewaretoken', getCSRF())		
	formData.append('current_entry', currentEntry)		
	if ($(subject).val().length > 0){
		formData.append('subject', $(subject).val())
	}
	if ($(body).val().length > 0){
		formData.append('body', $(body).val())
	}
	var postEntry = $.ajax({
		url: "/ajax/save_entry/",
		type: 'post',
		data: formData,
		contentType: false,
		processData: false,
		cache: false,
	})

	postEntry.done(function(data){
		currentEntry = data			
		if (callback) {
			callback()
		}
		$(ID).val(data)
		
		console.log('Success: Entry updated.')
	})

	postEntry.fail(function(data){
		console.log('Failed: Post Entry Data to Server.')
	})
}

var sendPhoto = function(photo, callback){		
	var formData = new FormData(photo)
	formData.append('csrfmiddlewaretoken', getCSRF())
	formData.append('entry_id', currentEntry)
	formData.append('photo', photo)		

	var postPhoto = $.ajax({
		url: "/ajax/add_entry_photo/",
		type: "post",
		data: formData,
		contentType: false,
		processData: false,
		cache: false,
	})

	postPhoto.done(function (result){			
		callback(result)
	})

	postPhoto.fail(function(result){
		console.log("failed")
	})
	
}		

var timedFunction;
var timer = 3000; // 3 secs

var resetTimer = function(){
	clearTimeout(timedFunction)
	timedFunction = setTimeout(saveEntry, timer)		
}

$('subject, body').on('change, keydown, keyup, keypress input', function(){	
	resetTimer()
})

$(body).focus(function(){
	$(this).autosize();
})



