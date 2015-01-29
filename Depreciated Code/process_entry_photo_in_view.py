#handel adding photo
if request.FILES:					
	uploaded_files = request.FILES.getlist('new-entry-photo')			
	invalids = request.POST['invalid-images'].split(',')			
	cleaned_files = false_files = []			
	
	if invalids == [u'']: #pass all files to check with PIL if no js error reported				
		cleaned_files = uploaded_files
	else: 
		result = entry.filter_javascript_invalid(uploaded_files, invalids)
		cleaned_files = result
		false_files += [image for image in uploaded_files if image not in cleaned_files]							
	
	failed = len(false_files)

	for image in cleaned_files:
		result = entry.process_entryphoto(image)
		if result[0] != True:
			failed += 1
			false_files.append(image)					
		else:
			EntryPhoto.objects.create(article = entry, image_file = result[1])

	if failed < len(uploaded_files):
		entry.update_last_edited_time()							

	if failed > 0: #print bad news to user.
		if failed == 1:
			msg = "A file cannot be uploaded, please try again with a valid JPG/GIF/PNG or BMP formatted image, (Max Size: 50MB)."
		else: 
			msg = "%s files cannot be uploaded, please try again with valid JPG/GIF/PNG or BMP formatted images, (Max Size: 50MB)." % failed
		messages.info(request, msg)
		messages.info(request, "Upload Failed:")
		for item in false_files:					
			messages.info(request, "%s | %.2f kb" %(item, item.size/1024.0))
		return redirect('diary:entry_edit_slug', entry_id = int(entry.id), slug = str(entry.slug))					