/*var editor = new MediumEditor('.editor')*/
$(document).ready(function(){				

	$('input[type="submit"]').click(function(e){
		e.preventDefault()					
		if ($('#final-date').val() == ""){
			fillPublishTimestamp()
		}
		var sub = $('input[name = "subject"]').val()
		var bod = $('textarea[name = "body"]').val()								
		if (sub.length == 0 && bod.length == 0) {
			var submitEmptyEntry = confirm("You're about to publish an empty entry, is it ok?")
			if (!submitEmptyEntry){
				return
			}
		}		
		$('#edit-entry-form').submit();
	})			

	// time picker related

	$('#test').click(function(){
		fillPublishTimestamp()
	})

	var pDate = rome(date, {
			weekStart: 1,
			time: false,	
		})		

	var pTime = rome(time, {			
		date: false,	
	})		
	
	var dateTimeToTimestamp = function(date, time){
		// date format 2015-01-27
		// time format 13:15:55
		timestamp = date + " " + time
		timestamp = moment(timestamp).unix()		
		return timestamp
	}
	

	var fillPublishTimestamp = function(){
		var dateStamp = moment().format('YYYY-MM-DD')
		var timeStamp = moment().format('HH:mm:ss')
		

		if (pTime.getDate() != null) {
			timeStamp = $('#time').val()			
		}		

		if (pDate.getDate() != null) {
			dateStamp = $('#date').val()			
			if (pTime.getDate() == null) {
				timeStamp = "00:00:00"
			}
		}		
		readableTime = moment(dateStamp + " " + timeStamp).calendar()
		$('#final-date').val(dateTimeToTimestamp(dateStamp, timeStamp))		
		return readableTime
		
	}

	$('#toggle-time-picker').click(function(){
		$('#publish-time').text('')
		$(this).hide()
		$('#time-picker').slideDown()		
	})

	$('#set-time').click(function(){
		$('#publish-time').text("Publish Date: " + fillPublishTimestamp());
		$('#toggle-time-picker').text('Change Publish Date');		
		$('#toggle-time-picker').show();		
		$('#time-picker').hide();
	})
})		