#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib import auth 
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from diary.models import Entry
# Create your views here.

@login_required
def index(request):

	
	msg = ''
				
	messageCode = {
		'1' : "<h1>Logged Out Successfully</h1>"
	}

	if request.GET.get('case','') in messageCode:
		msg = messageCode[request.GET['case']]

	else:
		msg = 'Get!'		

	entries = Entry.objects.all()	

	return render(request, 'diary/index.html', {'message': msg, 'entries': entries})

@login_required
def logout(request):	
	auth.logout(request)
	url = "%s?case=1" % reverse('diary:index')
	return redirect(url)

def login(request):

	if request.method == "POST":
		un = request.POST['login_username']
		pw = request.POST['login_password']		
		user = authenticate(username = un, password = pw)

		if user != None:
			auth.login(request, user)
			return redirect('diary:index')

		else:
			return render(request, 'diary/index.html', {'message': 'login-failed'})	

	else:
		return render(request, 'diary/login.html')

@login_required
def new_entry(request):
	if request.method == "POST":		
		sub = request.POST['new-subject']
		bod = request.POST['new-body']
		user = request.user

		newEntry = Entry(subject = sub, body = bod, author = user)
		newEntry.make_slug()
		newEntry.save()

		return redirect('diary:index')

	else:
		return render(request, 'diary/new_entry.html')


@login_required
def entry(request, entry_id, **slug):
	entry = Entry.objects.get(pk=entry_id)

	if slug:
		url_slug = slug.get('slug', False)
		if url_slug == False:
			return redirect(reverse('diary:index'))
		elif url_slug != entry.slug:
			return redirect(reverse('diary:index'))
	
	return render(request, 'diary/entry.html', {'entry': entry})

@login_required
def entry_edit(request, entry_id, **slug):
	entry = Entry.objects.get(pk=entry_id)

	if request.method == 'POST':		

		if request.POST['entry-delete'] == 'True':
			if request.user.is_superuser:				
				entry.delete()
				return redirect('diary:index')
			else:
				return redirect('http://facebook.com')

		sub = request.POST['entry-subject']
		bod = request.POST['entry-body']

		if sub != entry.subject:
			entry.update_subject(sub)

		if bod != entry.body:
			entry.update_body(bod)
		
		entry.save()

		return redirect('diary:entry', entry_id = int(entry.id))



	return render(request, 'diary/entry_edit.html', {'entry': entry})
