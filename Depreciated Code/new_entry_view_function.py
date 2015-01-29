def new_entry(request):
	if request.method == "POST":		
		sub = request.POST['new-subject']
		bod = request.POST['new-body']
		user = request.user

		if len(sub) * len(bod) == 0: #10000 * 0 = 0 
			messages.info(request, 'Please enter post title and body before submitting.')
			return render(request, 'diary/new_entry.html', {'subject': sub, 'body': bod})

		else: #text content ok, saving entry.
			newEntry = Entry(subject = sub, body = bod, author = user)
			newEntry.make_slug()
			newEntry.published = newEntry.edited = timezone.now()
			newEntry.save()
		
		if request.FILES: #file exists, handle 	

			uploaded_files = request.FILES.getlist('new-file')
			invalids = request.POST['invalid-images'].split(',')
			cleaned_files = false_files = []		


			if invalids == [u'']: #pass all files to check with PIL if no js error reported				
				cleaned_files = uploaded_files				
			else: 
				result = newEntry.filter_javascript_invalid(uploaded_files, invalids)
				cleaned_files = result
				false_files += [image for image in uploaded_files if image not in cleaned_files]				
			
			failed = len(false_files)

			for image in cleaned_files:
				result = newEntry.process_entryphoto(image)
				if result[0] != True:
					failed += 1
					false_files.append(image)					
				else:					
					EntryPhoto.objects.create(article = newEntry, image_file = result[1])

			if failed > 0: #print bad news to user.
				if failed == 1:
					msg = "A file cannot be uploaded, please try again with a valid JPG/GIF/PNG or BMP formatted image, (Max Size: 50MB)."
				else: 
					msg = "%s files cannot be uploaded, please try again with valid JPG/GIF/PNG or BMP formatted images, (Max Size: 50MB)." % failed
				messages.info(request, msg)
				messages.info(request, "Files not uploaded")
				for item in false_files:					
					messages.info(request, "%s | %.2f kb" %(item, item.size/1024.0))
				return redirect('diary:entry_edit_slug', entry_id = int(newEntry.id), slug = str(newEntry.slug))			

		return redirect('diary:entry_slug', entry_id = int(newEntry.id), slug = str(newEntry.slug) )

	else:
		return render(request, 'diary/new_entry.html')