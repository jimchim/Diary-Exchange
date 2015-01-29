#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.test import TestCase, Client
from diary.forms.diary_forms import registerForm
from diary.models import Entry, EntryPhoto
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import datetime
# Create your tests here.

class registerFormTest(TestCase):
	

	def test_create_form(self):
		form_data = {'username': 'foobar', 'email': 'a@example.com', 'password': '12345678', 'confirm_password': '12345678'}
		form = registerForm(data=form_data)
		self.assertEqual(form.is_valid(), True)

	def test_shortpassword_error(self):
		form_data = {'username': 'foobar', 'email': 'a@example.com', 'password': '123', 'confirm_password': '123'}
		form = registerForm(data = form_data)
		self.assertEqual(form.is_valid(), False)

	def test_shortpassword_error_message(self):
		form_data = {'username': 'foobar', 'email': 'a@example.com', 'password': '123', 'confirm_password': '123'}
		form = registerForm(data = form_data)
		response = self.client.post('/register/', form_data)

		#self.assertEqual(form.errors['password'], [u'Password too short, 8 characters minimum.'])
		self.assertFormError(response, 'form', 'password', 'Password too short, 8 characters minimum.')

	def test_duplicate_email(self):
		#form = registerForm(data = form_data)
		#form2 = registerForm(data = form_data)
		#self.assertEqual(form2.is_valid(), True)

		User1 = User.objects.create_superuser(username = 'Chris', email = 'a@example.com', password = '12345678')
		form_data = {'username': 'foobar', 'email': 'a@example.com', 'password': '12345678', 'confirm_password': '12345678'}
		response = self.client.post('/register/', form_data)
		self.assertFormError(response, 'form', 'email', 'Email already used by another account.')

class EntryPhotoTest(TestCase):

	def create_test_user(self):
		u = User.objects.create_superuser(username = 'Chris', email = 'a@example.com', password = '12345678')
		user = User.objects.first()
		return user

	def create_test_entry(self):
		u = User.objects.create_superuser(username = 'Jim', email = 'a@example.com', password = '12345678')
		user = User.objects.first()
		entry = Entry(subject = 'lakfjhsd', body = 'alskdjfh', author = user)
		entry.make_slug()
		entry.save()
		return entry	

	def test_entryphoto_processing_with_legit_jpg(self):
		""" standard JPG image """
		f = open('/home/jim/diaryexchange/diary/test/1.jpg', 'rb')
		data = f.read()
		newFile = SimpleUploadedFile('1.jpg', data)
		
		user = self.create_test_user()
		entry = self.create_test_entry()

		result = entry.process_entryphoto(newFile)
		EntryPhoto.objects.create(article = entry, image_file = result[1])
		img = EntryPhoto.objects.first()
		
		self.assertEqual(result[0], True) #upload success
		self.assertEqual(img.image_file.size, result[1].size) 	

	def test_entryphoto_processing_with_invalid_jpg(self):
		""" Text file with jpg extension, false image """
		f = open('/home/jim/diaryexchange/diary/test/test.jpg', 'rb')
		data = f.read()
		newFile = SimpleUploadedFile('1.jpg', data)
		
		user = self.create_test_user()
		entry = self.create_test_entry()

		result = entry.process_entryphoto(newFile)
		#EntryPhoto.objects.create(article = entry, image_file = result[1])
		#img = EntryPhoto.objects.first()
		
		self.assertEqual(result[0], "Cannot Open") #upload success
		#self.assertEqual(img.image_file.size, result[1].size) 	

	def test_entryphoto_processing_with_animated_gif(self):	
		""" Animated GIF image """
		f = open('/home/jim/diaryexchange/diary/test/2x.gif', 'rb')
		data = f.read()
		image = Image.open('/home/jim/diaryexchange/diary/test/4.gif')

		self.assertEqual((image.format, image.mode), ("GIF", "P"))

		newFile = SimpleUploadedFile('1.jpg', data)
		
		user = self.create_test_user()
		entry = self.create_test_entry()

		result = entry.process_entryphoto(newFile)
		convertedImageData = result[1].file
		f2 = open('temp.gif','wb')
		f2.write(convertedImageData.getvalue())
		f2.close()
		f2 = open('temp.gif','rb')		
		convertedImage = Image.open(f2)

		self.assertEqual(type(convertedImage), type(image))
		self.assertNotEqual(convertedImage, image)
		
		self.assertEqual(convertedImage.format, image.format)
		self.assertEqual(convertedImage.mode, image.mode) 
		#Animated GIF are still in P mode after processing... need to convert them into RGB in the future

		EntryPhoto.objects.create(article = entry, image_file = result[1])
		img = EntryPhoto.objects.first()

		#convertedImage = Image.open(img.image_file.url)
		
		self.assertEqual(result[0], True) #upload success		
		
	
	def test_entryphoto_processing_with_still_gif(self):
		""" standard GIF image """
		f = open('/home/jim/diaryexchange/diary/test/4.gif', 'rb')
		data = f.read()
		newFile = SimpleUploadedFile('1.jpg', data)
		
		user = self.create_test_user()
		entry = self.create_test_entry()

		result = entry.process_entryphoto(newFile)
		EntryPhoto.objects.create(article = entry, image_file = result[1])
		img = EntryPhoto.objects.first()
		
		self.assertEqual(result[0], True) #upload success		
		
	def test_entryphoto_processing_with_legit_png(self):
		""" standard RGB PNG image """
		f = open('/home/jim/diaryexchange/diary/test/back.png', 'rb')
		data = f.read()
		newFile = SimpleUploadedFile('1.jpg', data)
		
		user = self.create_test_user()
		entry = self.create_test_entry()

		result = entry.process_entryphoto(newFile)
		EntryPhoto.objects.create(article = entry, image_file = result[1])
		img = EntryPhoto.objects.first()
		
		self.assertEqual(result[0], True) #upload success
		#self.assertEqual(img.image_file.url, True)

	def test_entryphoto_processing_with_RGBA_png(self):
		""" PNG with Transparency Settings """
		f = open('/home/jim/diaryexchange/diary/test/12.png', 'rb')
		data = f.read()
		newFile = SimpleUploadedFile('1.jpg', data)
		
		user = self.create_test_user()
		entry = self.create_test_entry()

		result = entry.process_entryphoto(newFile)
		EntryPhoto.objects.create(article = entry, image_file = result[1])
		img = EntryPhoto.objects.first()
		
		self.assertEqual(result[0], True) #upload success
		#self.assertEqual(img.image_file.url, True)

	def test_entryphoto_processing_with_legit_bmp(self):
		""" standard BMP image """
		f = open('/home/jim/diaryexchange/diary/test/barbara.bmp', 'rb')
		data = f.read()
		newFile = SimpleUploadedFile('1.jpg', data)
		
		user = self.create_test_user()
		entry = self.create_test_entry()

		result = entry.process_entryphoto(newFile)
		EntryPhoto.objects.create(article = entry, image_file = result[1])
		img = EntryPhoto.objects.first()
		
		self.assertEqual(result[0], True) #upload success

class CreateEntryTest(TestCase):
	def create_test_user(self):
		""" helper method """
		u = User.objects.create_superuser(username = 'Chris', email = 'a@example.com', password = '12345678')
		user = User.objects.first()
		return user	

	def test_create_entry_without_specifying_slug(self):
		""" test overriden save method is working and calling make_sulg method automatically."""
		user = self.create_test_user()
		entry = Entry.objects.create(author = user, subject = "lkajsfhd", body = "laksjdhf" )		
		self.assertEqual(entry.slug, "lkajsfhd")

	def test_create_entry_without_slug_and_subject(self):
		""" test if entry gets untitled as subject if not specified"""
		user = self.create_test_user()
		entry = Entry.objects.create(author = user, body = "laksjdhf" )				
		self.assertEqual(entry.slug, "untitled")

	def test_create_entry_without_giving_subject(self):
		""" test if entry gets untitled as subject if not specified"""
		user = self.create_test_user()
		entry = Entry.objects.create(author = user, body = "laksjdhf" )				
		self.assertEqual(entry.subject, "Untitled")

class EntryViewTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_superuser(username = 'spam', email = 'asfd@askljf.com', password = '12345678')
		self.user2 = User.objects.create_superuser(username = 'jim', email = 'jim@askljf.com', password = '12345678')
		self.user1_post = Entry.objects.create(subject = 'Entry 1', body = 'body', author = self.user, is_draft = False)
		tomorrow = datetime.date.today() + datetime.timedelta(days = 1)
		self.user1_post2 = Entry.objects.create(subject = 'Future Entry', body = 'body', author = self.user, is_draft = False, published = tomorrow)
		self.user2_post = Entry.objects.create(subject = 'Entry 2', body = 'body', author = self.user2, is_draft = True)
		self.client = Client()
		self.login_data = {
			'login_username': 'spam',
			'login_password': '12345678',
		}

	def test_login_page(self):
		response = self.client.get('/login/')
		self.assertEqual(response.status_code, 200) #200 OK		
		self.assertTemplateUsed(response, 'base.html')
		self.assertTemplateUsed(response, 'diary/login.html')

	def test_logging_in(self):		
		response = self.client.post('/login/', self.login_data, follow = True)				
		self.assertTemplateUsed(response, 'diary/index.html')
		self.assertTemplateUsed(response, 'base.html')
		self.assertRedirects(response,'/')		
		self.assertEqual(response.context['user'], self.user) #response.context['user'] == request.user	

	def test_access_index_without_login(self):
		response = self.client.get('/profile/', follow = True)		
		self.assertTemplateUsed(response, 'diary/login.html')
		self.assertTemplateNotUsed(response, 'diary/profile.html')
		self.assertRedirects(response, '/login/?next=/profile/')

	def test_entry_viewed_by_author(self):
		self.client.login(username = 'spam', password = '12345678')		
		user1_post_url = '/entry/%s' % self.user1_post.id
		response = self.client.get(user1_post_url, follow = True)
		self.assertEqual(response.context['user'], self.user1_post.author)
		self.assertTemplateUsed(response, 'diary/entry.html')
		
	def test_entry_viewed_by_others(self):
		self.client.login(username = 'jim', password = '12345678')		
		user1_post_url = '/entry/%s' % self.user1_post.id
		response = self.client.get(user1_post_url, follow = True)
		self.assertNotEqual(response.context['user'], self.user1_post.author)
		self.assertTemplateUsed(response, 'diary/entry.html')					

	def test_entry_draft_cannot_be_seen_in_index(self):
		self.client.login(username = 'spam', password = '12345678')
		response = self.client.get('/')
		self.assertContains(response, self.user1_post.subject)
		self.assertNotContains(response, self.user2_post.subject)

	def test_entry_draft_can_be_seen_in_profile_by_author(self):
		self.client.login(username = 'jim', password = '12345678')
		response = self.client.get('/profile/')
		self.assertContains(response, self.user2_post.subject)

	def test_profile_contains_entry_created_by_logged_in_users_only(self):
		self.client.login(username = 'jim', password = '12345678')
		response = self.client.get('/profile/')
		self.assertNotContains(response, self.user1_post.subject)		

	def test_logout_redirect_to_login(self):
		self.client.login(username = 'jim', password = '12345678')
		response = self.client.get('/logout/', follow = True)
		self.assertRedirects(response, '/login/')
		self.assertTemplateUsed(response, 'diary/login.html')

	#test entry edit

	def test_entry_edit_viewed_by_author(self):
		self.client.login(username = 'spam', password = '12345678')
		user1_entry_edit_url = '/entry/edit/%s' % self.user1_post.id		
		response = self.client.get(user1_entry_edit_url, follow = True)
		self.assertEqual(response.context['user'], self.user1_post.author)
		self.assertTemplateUsed(response, 'diary/entry_edit.html')		

	def test_entry_cannot_be_edited_by_others(self):
		self.client.login(username = 'jim', password = '12345678')
		user1_entry_edit_url = '/entry/edit/%s' % self.user1_post.id		
		response = self.client.get(user1_entry_edit_url, follow = True)
		self.assertNotEqual(response.context['user'], self.user1_post.author)
		self.assertTemplateUsed(response, 'diary/index.html') # unauthorized user are redirected to the previous page		

	#end test entry edit

	# test entry delete

	def test_entry_can_be_deleted_by_author(self):
		self.client.login(username = 'spam', password = '12345678')
		response = self.client.post('/entry/delete/', {'entry-id': self.user1_post.id}, follow = True)
		self.assertRedirects(response, '/')		

	def test_entry_are_actually_deleted_by_author(self):
		self.client.login(username = 'spam', password = '12345678')
		response = self.client.get('/')
		self.assertContains(response, self.user1_post.subject)
		response = self.client.post('/entry/delete/', {'entry-id': self.user1_post.id}, follow = True)
		self.assertRedirects(response, '/')
		self.assertNotContains(response, self.user1_post.subject)		

	def test_entry_can_not_be_deleted_by_others(self):
		self.client.login(username = 'jim', password = '12345678')
		response = self.client.post('/entry/delete/', {'entry-id': self.user1_post.id}, follow = True)		
		self.assertEqual(response.status_code, 400)
		self.assertContains(response, 'Error: Entries can only be deleted by the author.', status_code=400)		

	def test_entry_are_actually_not_deleted_by_others(self):
		self.client.login(username = 'jim', password = '12345678')
		response = self.client.get('/')
		self.assertContains(response, self.user1_post.subject)
		response = self.client.post('/entry/delete/', {'entry-id': self.user1_post.id}, follow = True)
		self.assertContains(response, 'Error: Entries can only be deleted by the author.', status_code=400)		
		response = self.client.get('/')
		self.assertContains(response, self.user1_post.subject, )		

	# end test entry delete
		
	def test_entry_can_be_viewed_with_correct_entry_id_and_slug(self):
		self.client.login(username = 'spam', password = '12345678')				
		response = self.client.get('/entry/%s/%s/' % (self.user1_post.id, self.user1_post.slug))
		self.assertTemplateUsed(response, 'diary/entry.html')

	def test_entry_CANNOT_be_viewed_with_correct_entry_id_and_slug(self):
		self.client.login(username = 'spam', password = '12345678')				
		response = self.client.get('/entry/%s/%s/' % (self.user1_post.id, "this-is-madness!"))
		self.assertEqual(response.status_code, 404)

	def test_entry_set_to_post_in_the_future_cannot_be_seen_publicly(self):
		self.client.login(username = 'spam', password = '12345678')				
		response = self.client.get('/')	#public
		self.assertNotContains(response, 'Future Entry')		
		future_entry = Entry.objects.get(subject = 'Future Entry')
		self.assertEqual(future_entry.author, response.context['user'])
		
	def test_entry_set_to_post_in_the_future_can_be_seen_privately(self):
		self.client.login(username = 'spam', password = '12345678')				
		response = self.client.get('/profile/') #private
		self.assertContains(response, 'Future Entry')
		future_entry = Entry.objects.get(subject = 'Future Entry')
		self.assertEqual(future_entry.author, response.context['user'])	

	