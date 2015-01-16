from django.test import TestCase
from diary.forms.diary_forms import registerForm
from diary.models import Entry, EntryPhoto
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
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
		f = open('/home/jim/diaryexchange/diary-exchange/diary/test/1.jpg', 'rb')
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
		f = open('/home/jim/diaryexchange/diary-exchange/diary/test/test.jpg', 'rb')
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
		f = open('/home/jim/diaryexchange/diary-exchange/diary/test/2x.gif', 'rb')
		data = f.read()
		image = Image.open('/home/jim/diaryexchange/diary-exchange/diary/test/4.gif')

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
		f = open('/home/jim/diaryexchange/diary-exchange/diary/test/4.gif', 'rb')
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
		f = open('/home/jim/diaryexchange/diary-exchange/diary/test/back.png', 'rb')
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
		f = open('/home/jim/diaryexchange/diary-exchange/diary/test/12.png', 'rb')
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
		f = open('/home/jim/diaryexchange/diary-exchange/diary/test/barbara.bmp', 'rb')
		data = f.read()
		newFile = SimpleUploadedFile('1.jpg', data)
		
		user = self.create_test_user()
		entry = self.create_test_entry()

		result = entry.process_entryphoto(newFile)
		EntryPhoto.objects.create(article = entry, image_file = result[1])
		img = EntryPhoto.objects.first()
		
		self.assertEqual(result[0], True) #upload success
