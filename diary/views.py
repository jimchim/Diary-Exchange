#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib import auth 
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime
from diary.models import Entry, EntryPhoto, UserUploadedPhoto
from diary.forms.diary_forms import registerForm
from PIL import Image

import os, sys
# Create your views here.


def login(request):
	nextPage = '/' #just to be safe

	if request.method == "POST":
		un = request.POST['login_username']
		pw = request.POST['login_password']		
		user = authenticate(username = un, password = pw)
		nextPage = request.GET.get('next',"/")

		if user != None:
			auth.login(request, user)
			if nextPage == '/':
				messages.success(request, 'Logged in')
				return redirect('diary:index')				
			else:				
				# messages.info(request, 'Redirecting you to the previous page')
				return redirect(nextPage)				

		else:		
			return render(request, 'diary/login.html', {'message': 'Login Failed'})	

	if request.GET:
		nextPage = request.GET.get("next",'/')

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
	return redirect('diary:login')


@login_required
def index(request):		
	messages.info(request, request.META.get('HTTP_REFERER', ""))
	entries = Entry.objects.filter(is_draft = False).filter(published__lte = timezone.now()).order_by('-published')			
	return render(request, 'diary/index.html', {'entries': entries})


@login_required
def new_entry(request):
	if request.method == "GET":		
		#request.session['current_entry'] = None
		return render(request, 'diary/new_entry.html', {'years': range(1991, datetime.now().year)})

	elif request.method == "POST":				
		entry = None

		try:
			entry = Entry.objects.get(pk = request.POST.get('entry-id'))
		except:
			entry = Entry()		

		entry.subject = request.POST.get('subject', "")
		entry.body = request.POST.get('body', "")
		entry.author = request.user
		entry.is_draft = False #need to set this to make it publicly available
		entry.published = datetime.fromtimestamp(int(request.POST.get('timestamp', "")))		
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

		if request.POST.get('current_entry', "false") == "false": #new entry
			entry = Entry.objects.create(subject = subject, body = body, author = request.user)			
			return HttpResponse(entry.id)	 

		else: #update entry		
			entry = Entry.objects.get(pk = request.POST.get('current_entry'))
			if entry.subject != subject:
				entry.subject = subject				
			if entry.body != body:
				entry.body = body				
			entry.save()			
			return HttpResponse(entry.id)	 					
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
	entry = get_object_or_404(Entry, pk = entry_id)		
	if slug and slug.get('slug') != entry.slug:
		raise Http404

	if entry.published > timezone.now() and request.user != entry.author:
		raise Http404	
	
	return render(request, 'diary/entry.html', {'entry': entry})


@login_required
def entry_delete(request):
	error_message = ""
	if request.method == 'POST':
		try:
			entry = Entry.objects.get(pk = request.POST.get('entry-id'))			
			if request.user == entry.author:
				entry.self_destruction()
				return redirect('diary:index')
			else:
				error_message = "Error: Entries can only be deleted by the author."
		except:
			error_message = "Error: Entry does not exist."		

		response = render(request, 'base.html', {'error_message': error_message})
		return HttpResponseBadRequest(response)
	else:
		raise Http404


@login_required
def entry_edit(request, entry_id, **slug):
	entry = get_object_or_404(Entry, pk=entry_id)	
	if slug and slug.get('slug') != entry.slug: #slug in url should match entry's slug		
		raise Http404

	if request.user != entry.author:
		messages.info(request, 'Entries can only be edited by the author.')
		return redirect(request.META.get('HTTP_REFERER', "/"))


	if request.method == "GET":
		return render(request, 'diary/entry_edit.html', {'entry': entry})		

	if request.method == 'POST':		
		#handle subject and body change, edited time is updated if changes presence
		sub = request.POST.get('subject', entry.subject)
		bod = request.POST.get('body', entry.body)		
		if sub != entry.subject:
			entry.update_subject(sub)

		if bod != entry.body:
			entry.update_body(bod)
		
		entry.save() #changed or not, save it.
		return redirect('diary:entry_slug', entry_id = int(entry.id), slug = str(entry.slug) ) #go to entry after update	


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
		try:
			entry = Entry.objects.get(pk = request.POST.get('entry_id',None))
		except:
			return HttpResponseBadRequest('Error: Cannot attach entry photo to a valid entry.')		

		if entry.author != request.user:
			return HttpResponseBadRequest('Error: Only the author may update/edit an entry.')					

		if request.FILES and len(request.FILES) == 1:			
			result = entry.process_entryphoto(request.FILES['photo'])
			if result[0] == True: #safe to save as photo
				photo = EntryPhoto.objects.create(article = entry, image_file = result[1])
				return HttpResponse(photo.image_file.url)				
			else:					
				return HttpResponse("Error: Failed")				
		else:
			return HttpResponseBadRequest('Error: Cannot process more than 1 photo at a time.')			
	else:
		raise Http404

def test(request):
	message = "You're at test page"
	message = ""
	filelist = []
	for filename in os.listdir('./media/compressed'):
		filelist.append(filename)
		#message += "<img src = >" + filename + "</p>"
	
	#return HttpResponse(message)
	return render(request, 'diary/test.html', {'files': filelist})


@login_required
def profile(request):
	entries = request.user.entry_set.all().order_by('-published')
	return render(request, 'diary/profile.html', {'entries': entries})