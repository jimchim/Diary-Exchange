$(document).ready(function(){

	getCookie = function(name) {
		var cookieValue = null;
		if (document.cookie && document.cookie != '') {
			var cookies = document.cookie.split(';');
			for (var i = 0; i < cookies.length; i++) {
				var cookie = jQuery.trim(cookies[i]);
				// Does this cookie string begin with the name we want?
				if (cookie.substring(0, name.length + 1) == (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}

	getCSRF = function(){
		return getCookie('csrftoken')
	}

	/* Image Validation Helper Function */

	validateImage = function(imageFile, callback) {
		var reader = new FileReader()
		var image = new Image() // Image object used to test the uploaded image file

		reader.readAsDataURL(imageFile)

		reader.onloadend = function(){
			// when reader object loaded the image file successfully, do the following.
			image.src = reader.result // load Image object with reader.result (an url used as src attribute)
			image.onload = function(_image){
				callback(imageFile, image)
				// if successfulling validated the image is an image, return the image object				
			}
			image.onerror = function(){
				callback(imageFile.name)
				//return the name of the image to callback if not an valida image.				
			}					
		} 		
	}	


	isAcceptedImageFile = function(file){
		if (isValidSize(file.size) && isValidImageFormat(file.name)){
			return true
		}

		else {
			return false
		}
	}

	isValidImageFormat = function(imageName){
		var allowedFormat = ['jpg', 'jpeg', 'gif','png','bmp']
		var extension = imageName.split('.').pop().toLowerCase() // ensure match with lowercased allowedFormat
		
		if ( allowedFormat.indexOf(extension) == -1 ) {  // not in allowed formats
			
			//invalidFiles.push(file) 
			return false
			//return (imageName + ' is not in a supported file format, please upload JPG / GIF / PNG or BMP images only.')
		}

		else {
			return true
		}
	}

	isValidSize = function(fileSize){
		var sizeInMB = fileSize/1024/1024
		if (sizeInMB >= 30) { 
			//invalidFiles.push(file) 
			return false
			//return (name + ' is too big, please upload images under 30 MBs.')
		}
		else {
			return true
		}			
	}
	/* END Image Validation Helper Function */	

	/* DOM Control Helper Function*/

	appendImage = function(location, imageSRC){
		imageElement = "<img src = '" + imageSRC + "'>"
		$(location).append(imageElement)
	}

	showToastWarning = function(message){
		bsAlertCode = "<div class='alert alert-dismissible alert-warning' role='alert'><button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button><p>" + String(message) + "</p></div>"
		$('#page-content').prepend(bsAlertCode)		
	}


	/* END DOM Control Helper Function*/
})/*END DOCUMENT READY*/