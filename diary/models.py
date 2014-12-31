#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils import timezone
from unidecode import unidecode
import urllib

# Create your models here.
class Entry(models.Model):
	"""docstring for ClassName"""
	subject = models.CharField(max_length = 180)
	body = models.TextField()
	slug = models.SlugField()
	author = models.ForeignKey(User)
	
	published = models.DateTimeField('Time Published', default= timezone.now())
	edited = models.DateTimeField('Time Edited', default=timezone.now())
	is_draft = models.BooleanField(default=True)
	is_public = models.BooleanField(default=False)

	def __unicode__(self):
		return self.subject


	def make_slug(self):
		""" create slug using self.subject """
		sub = self.subject

		#if type(sub) == 'unicde':
		sub = unidecode(sub)
		sub = slugify(sub)		
		self.slug = slugify(sub)

		return sub



	def change_last_edited_time(self):
		""" update edited field 
			short cut function for object update functions
		"""
		self.edited = timezone.now()

	def update_body(self, newBody):
		self.body = newBody
		self.change_last_edited_time()

	def update_subject(self, newSubject):
		self.subject = newSubject
		self.change_last_edited_time()