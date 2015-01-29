#handle remove photo, clean passed photo ids
selected_photos = request.POST['selected-entry-photo']

if len(selected_photos) > 0:
	selected_photos = selected_photos.split(',')
	photoIDs = []
	for photoID in selected_photos:
		if len(photoID) > 0:
			try:
				photoIDs.append(int(photoID))
			except ValueError:
				return redirect('diary:entry', entry_id = int(entry.id))

	try:	
		entry.remove_entry_photos_by_ids(photoIDs)				
	except:
		return redirect('diary:entry', entry_id = int(entry.id))			