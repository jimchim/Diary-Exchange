#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib import auth 
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from diary.models import Entry, EntryPhoto, UserUploadedPhoto
from diary.forms.diary_forms import registerForm
from PIL import Image
# Create your views here.


def login(request):
	nextPage = '/' #just to be safe

	if request.method == "POST":
		un = request.POST['login_username']
		pw = request.POST['login_password']		
		user = authenticate(username = un, password = pw)
		nextPage = request.GET['next']

		if user != None:
			auth.login(request, user)
			if nextPage == '/':
				messages.success(request, 'Logged in')
				return redirect('diary:index')				
			else:				
				messages.info(request, 'Redirecting you to the previous page')
				return redirect(nextPage)				

		else:		
			return render(request, 'diary/login.html', {'message': msg})	

	if request.GET:
		nextPage = request.GET['next']

	return render(request, 'diary/login.html', {'next': nextPage})


def register(request):

	form = registerForm()

	if request.method == 'POST':
		form = registerForm(request.POST)
		if form.is_valid():			
			data = form.cleaned_data
			messages.info(request, "The form is valid %s" % data)			
			return redirect('diary:register')				
	return render(request, 'diary/register.html', {'form' : form})


@login_required
def logout(request):	
	auth.logout(request)	
	return redirect('diary:index')


@login_required
def index(request):		
	entries = Entry.objects.filter(is_draft = False).order_by('-published')			
	return render(request, 'diary/index.html', {'entries': entries})


@login_required
def new_entry(request):
	if request.method == "GET":		
		request.session['current_entry'] = None
		return render(request, 'diary/new_entry.html')
	elif request.method == "POST":				
		entry = None
		if request.session['current_entry'] != None: #Entry was created by Ajax call to save the draft
			entry = Entry.objects.get(pk = request.session['current_entry'])
		else:
			entry = Entry()		
		entry.subject = request.POST.get('subject', "")
		entry.body = request.POST.get('body', "")
		entry.author = request.user
		entry.is_draft = False #need to set this to make it publicly available
		entry.save()

		return redirect('diary:entry_slug', entry_id = int(entry.id), slug = str(entry.slug))		

	else:
		raise Http404
		
		
@login_required
def save_entry(request):
	""" This view process entry saving POSTed by Ajax
		The Ajax call is triggered when the user changed the content of a post,
		then idled for 3 seconds.

		Note: Only JavaScript checking is implemented, need to set timeout on
		server side as well in the future to lower the threat of DDoS attack.
	"""
	if request.method == "POST" and request.is_ajax():	
		entry = None
		subject = request.POST.get('subject', "")
		body = request.POST.get('body', "")

		if request.session['current_entry'] == None: #new entry
			entry = Entry.objects.create(subject = subject, body = body, author = request.user)
			request.session['current_entry'] = entry.id
			return HttpResponse(entry.id)	 

		else: #update entry		
			entry = Entry.objects.get(pk = request.session['current_entry'])			
			if entry.subject != subject:
				entry.subject = subject				
			if entry.body != body:
				entry.body = body				
			entry.save()			
			return HttpResponse("entry updated")	 					
	else:
		raise Http404		

@login_required
def entry(request, entry_id, **slug):
	""" 
		Slug is an optional keyword argument when parsing the url pattern in urls.py
		this view function means that the url can be simply foo.com/entry_id
		or foo.com/entry_id/slug
		where entry_id is required in both cases in order to avoid url clashing
		(slug might not be unique in all entries)
	"""
	entry = Entry.objects.get(pk=entry_id)

	if slug:
		url_slug = slug.get('slug', False)
		if url_slug == False:
			return redirect(reverse('diary:index'))
		elif url_slug != entry.slug:
			return redirect(reverse('diary:index'))

	if entry.entryphoto_set.count() > 0:
		entry_photos = entry.entryphoto_set.all()
		return render(request, 'diary/entry.html', {'entry': entry, 'entry_photos': entry_photos})	
	
	return render(request, 'diary/entry.html', {'entry': entry})


@login_required
def entry_edit(request, entry_id, **slug):
	entry = Entry.objects.get(pk=entry_id)

	if request.method == 'POST':		

		if request.POST['entry-delete'] == 'True' and request.user.is_superuser:			
			entry.self_destruction()							
			return redirect('diary:index')

		else:
			messages.info(request, "You do not have permission to delete this post.") 
			
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

		#handle subject and body change, edited time is updated if changes presence
		sub = request.POST['entry-subject']
		bod = request.POST['entry-body']		

		if sub != entry.subject:
			entry.update_subject(sub)

		if bod != entry.body:
			entry.update_body(bod)

		entry.save()

		return redirect('diary:entry_slug', entry_id = int(entry.id), slug = str(entry.slug) ) #go to entry after update

	return render(request, 'diary/entry_edit.html', {'entry': entry})


def check_username(request):	

	if request.method == 'GET' and request.is_ajax():		
		if request.GET.get('username',None):
			username = request.GET['username']
			try:
				used = User.objects.get(username = username)
				used = True
			except User.DoesNotExist:
				used = False								
			return HttpResponse(used) 
		else:
			return HttpResponse('No Valid Data Submitted by Ajax') 
	else:
		response = render(request, 'base.html', { "error_message": "Nothing to see here, please move along :P"} )
		return HttpResponseBadRequest(response)
		#raise Http404
		#return redirect('diary:index')

@login_required
def add_entry_photo(request):	
	if request.method == 'POST' and request.is_ajax():

		entry = None
		if request.session['current_entry'] == None:
			entry = Entry.objects.create(subject = request.POST.get('subject', ""), body = request.POST.get('body',""), author = request.user)
		else:
			entry = Entry.objects.get(pk = request.session['current_entry'])

		if request.FILES and len(request.FILES) == 1:			
			result = entry.process_entryphoto(request.FILES['photo'])
			if result[0] == True: #safe to save as photo
				photo = EntryPhoto.objects.create(article = entry, image_file = result[1])
				return HttpResponse(photo.image_file.url)				
			else:					
				return HttpResponse("Failed")				
		else:
			return HttpResponseBadRequest('Cannot process more than 1 photo at a time.')			
	else:
		raise Http404

def test(request):
	return HttpResponse("You're at test page")


@login_required
def profile(request):
	entries = request.user.entry_set.all().order_by('-published')
	return render(request, 'diary/profile.html', {'entries': entries})