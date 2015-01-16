#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils import timezone

from unidecode import unidecode
from PIL import Image
from StringIO import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import urllib
import os
import uuid

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

	def update_last_edited_time(self):
		""" update edited field 
			short cut function for object update functions
		"""
		self.edited = timezone.now()

	def update_body(self, newBody):
		self.body = newBody
		self.update_last_edited_time()

	def update_subject(self, newSubject):
		self.subject = newSubject
		self.update_last_edited_time()

	#def remove_entry_photo(self,)

	def get_all_photoset_image_ids(self):
		photoset_ids = [photo.id for photo in self.entryphoto_set.all()]
		return photoset_ids

	def is_in_photoset(self, photoID):
		photo_set_ids = self.get_all_photoset_image_ids()
		if photoID in photo_set_ids:
			return True
		else:
			return False		

	#build a function that takes a list of entryphoto id, check if they are in this entry's entryphoto_set, if so, delete it.

	def delete_photoset_image(self,photoID):
		if self.is_in_photoset(photoID):
			image = self.entryphoto_set.get(pk = photoID)
			image_file = image.image_file

			storage = image_file.storage
			path = image_file.path

			storage.delete(path) #delete file
			image.delete() #delete record

			return True
		else:
			return False

	def remove_entry_photos_by_ids(self,photoIDs = []):
		"""
			delete entry photos from entryphoto_set with a list of IDs,
			if the photo with a passed ID is not part of the entryphoto_set,
			the photo will not be deleted.

			!! Make sure the IDs passed into this function are integer
		"""
		for photoID in photoIDs:
			if self.delete_photoset_image(photoID): #successfully deleted
				#print "EntryPhoto with Primary Key: %i is deleted" % photoID
				continue
			else:				
				#print 'Photo not in entryphoto_set, deletion failed'
				raise self.DoesNotExist				
				break	


	def filter_javascript_invalid(self,uploads,invalids):
		""" 
		Takes a list of uploaded item  and a list of invalid items reported by javascript
		return list of qualified items

		"""		
		cleaned_files = [] 		

		for item in uploads:					
			if item.name not in invalids: #only process js validated images on server to save resource										
				cleaned_files.append(item)

		return cleaned_files


	def process_entryphoto(self, image):
		""" 
		Takes an image file and validate, compress and convert it,
		returns the result.
		"""		
		if image.size/1024.0/1024 > 50: #MB
			return "Too Big", image.name
		
		acceptedPILFormat = ['JPEG','PNG','BMP','GIF']

		try:
			img = Image.open(image)
		except IOError:
			return "Cannot Open", image.name
		else:
			if img.format in acceptedPILFormat:
				img.thumbnail((1024,1024), Image.ANTIALIAS)
				imageString = StringIO()				
				if img.mode != 'RGB':
					name = ('temp.' + img.format).lower()
					img.save(imageString,format = img.format, optimize = True)
					imagefile = InMemoryUploadedFile(imageString, None, name, 'image/jpeg', imageString.len, None)					
				else:
					img.save(imageString,format = "JPEG", optimize = True)
					imagefile = InMemoryUploadedFile(imageString, None, 'temp_name.jpg', 'image/jpeg', imageString.len, None)
				#newPhoto = EntryPhoto.objects.create(image_file = imagefile, article = self)		
				return True, imagefile				
			else:
				return "Invalid Format", image.name 
		

	def add_entryphoto(self, images_list):		#not using this method to add photo anymore.
		invalid_image = 0
		for image in images_list:				
			if self.save_entryphoto(image):
				continue
			else:
				invalid_image += 1					
				#raise BaseException

		if invalid_image == 0:
			return 'all uploaded'

		return invalid_image

	def self_destruction(self):
		photoIDs = [image.id for image in self.entryphoto_set.all()]
		print photoIDs
		self.remove_entry_photos_by_ids(photoIDs)
		self.delete()


def uuid_filename(instance, filename):
	extension = filename.split('.')[-1] #get last piece
	filename = "%s.%s" % (uuid.uuid4().hex, extension)
	return os.path.join('entry_photo', filename)

class EntryPhoto(models.Model):
	article = models.ForeignKey(Entry)	
	image_file = models.ImageField(upload_to = uuid_filename)