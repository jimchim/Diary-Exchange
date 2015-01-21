/*var editor = new MediumEditor('.editor')*/
$(document).ready(function(){				
	entryCreated = false

	$('textarea[name="body"]').hide();	

	var saveEntry = function(){
		var formData = new FormData()
		formData.append('csrfmiddlewaretoken', getCSRF())		
		if ($('input[name="subject"]').val().length > 0){
			formData.append('subject', $('input[name="subject"]').val())
		}
		if ($('textarea[name="body"]').val().length > 0){
			formData.append('body', $('textarea[name="body"]').val())
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
			entryCreated = true
			console.log(data)
			//console.log('Success: Posted Entry Data to Server')
		})

		postEntry.fail(function(data){
			console.log('Failed: Post Entry Data to Server')
		})
	}

	var timedFunction;
	var timer = 3000;

	var resetTimer = function(){
		clearTimeout(timedFunction)
		timedFunction = setTimeout(saveEntry, timer)		
	}

	$('input[name="subject"], textarea[name="body"]').on('change, keydown, keyup, keypress input', function(){
		resetTimer()
	})

	var alertData = function(){		
		subjectData = $('input[name="subject"]').val()
		bodyData = $('textarea[name="body"]').val()
		/*console.log("subject: " + subjectData)
		console.log("body: " + bodyData)*/
	}
	

	var sendPhoto = function(photo, callback){
		var formData = new FormData(photo)
		formData.append('csrfmiddlewaretoken', getCSRF())
		formData.append('photo', photo)
		if (!entryCreated) { // entryphoto needs an entry as FK to save.
			if ($('input[name="subject"]').val().length > 0){
				formData.append('subject', $('input[name="subject"]').val())
			}
			if ($('textarea[name="body"]').val().length > 0){
				formData.append('body', $('textarea[name="body"]').val())
			}			
		}
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
	

	$('#test').click(function(){		
		console.log('test button clicked')		
	})
	
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
})		