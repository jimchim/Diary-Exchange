#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib import auth 
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages

from diary.models import Entry, EntryPhoto
from diary.forms.diary_forms import registerForm
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
			messages.info(request, "The form is valid <br>%r" % data)
			return redirect('diary:register')

	return render(request, 'diary/register.html', {'form' : form})

@login_required
def logout(request):	
	auth.logout(request)	
	return redirect('diary:index')

@login_required
def index(request):		
	entries = Entry.objects.all().order_by('-published')			
	return render(request, 'diary/index.html', {'entries': entries})


@login_required
def new_entry(request):
	if request.method == "POST":		
		sub = request.POST['new-subject']
		bod = request.POST['new-body']
		user = request.user

		newEntry = Entry(subject = sub, body = bod, author = user)
		newEntry.make_slug()
		newEntry.published = newEntry.edited = timezone.now()
		newEntry.save()
		
		if request.FILES:			
			try:
				uploaded_files = request.FILES.getlist('new-file')
				newEntry.add_entryphoto(uploaded_files)							
			except:
				return render(request, 'diary/new_entry.html')


		return redirect('diary:index')

	else:
		return render(request, 'diary/new_entry.html')


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
			print "You do not have permission to delete this post."
			
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
			try:
				uploaded_files = request.FILES.getlist('new-entry-photo')
				entry.add_entryphoto(uploaded_files)						
				entry.update_last_edited_time()							
			except:
				return redirect('diary:entry', entry_id = int(entry.id))

		#handle subject and body change, edited time is updated if changes presence
		sub = request.POST['entry-subject']
		bod = request.POST['entry-body']		

		if sub != entry.subject:
			entry.update_subject(sub)

		if bod != entry.body:
			entry.update_body(bod)

		entry.save()

		return redirect('diary:entry', entry_id = int(entry.id)) #go to entry after update

	return render(request, 'diary/entry_edit.html', {'entry': entry})