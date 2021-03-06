from django.db import models


#>>>>>>>>> REUSABLE <<<<<<<<<

# the contents of a tab.
 # It is located at the top of the page.
site_tabs = (
	('start', 'start'),
	('portrety', 'portrety'),
	('okolicznosciowe', 'okolicznosciowe'),
	('rodzinne', 'rodzinne'),
	('sensualne', 'sensualne'),
	('wiecej', 'wiecej'),
	)


#	The model for the page description and additional information for customers.
class DescriptionReusable(models.Model):
	title = models.CharField(max_length=50, blank=True)
	content = models.TextField(blank=True)
	site_tab = models.CharField(max_length=30, choices=site_tabs)



	def __str__(self):
		return self.title


# 		The model that saves photos
class PhotoPortfolio(models.Model):
	columns= ( # Three columns with photos on the page
		('kolumna1', 'kolumna1'),
		('kolumna2', 'kolumna2'),
		('kolumna3', 'kolumna3'),
		)
	photo = models.ImageField(upload_to='reusable_photo', blank=True, null=True)
	photo_theme = models.CharField(max_length=50, blank=True, help_text='Morze być puste')	
	column = models.CharField(max_length=20, choices=columns)
	seat_number = models.CharField(max_length=40) # the place of the photo in the column.
	site_tab = models.CharField(max_length=30, choices=site_tabs)

	# Overriding the save method so that when an image is deleted or updated,
    # the old image is deleted from the storage	

	def save(self, *args, **kwargs):
		if self.pk:
			old_record = PhotoPortfolio.objects.get(pk=self.pk)
			if old_record.photo != self.photo:
				old_record.photo.delete(save=False)
		super(PhotoPortfolio, self).save(*args, **kwargs)

	def __str__(self):
		name = self.site_tab + ' ' + self.photo.name[15:]
		return name


#>>>>>>>>>> BLOG <<<<<<<<<<

class FirstArticle(models.Model):
	art_photo = models.ImageField(null=True, blank=True, upload_to='blog_photo')
	art_title = models.CharField(max_length=50)	
	art_text = models.TextField()

	def __str__(self):
		return self.art_title

	# Overriding the save method so that when an image is deleted or updated,
    #           the old image is deleted from the storage
	def save(self, *args, **kwargs):
		if self.pk:
			old_record = FirstArticle.objects.get(pk=self.pk)
			if old_record.art_photo != self.art_photo:
				old_record.art_photo.delete(save=False)
		super(FirstArticle, self).save(*args, **kwargs)

 # adding an imageURL method to exclude an error if the image is missing
	@property
	def imageUrl(self):
		try:
			im = self.art_photo.url
		except:
			im = ''
		return im


class ArticleTitle(models.Model):	
	art_title = models.CharField(max_length=50, unique=True)
	title_font = models.CharField(max_length=5, blank=True)
	title_photo = models.ImageField(upload_to='blog_photo', blank=True)
	piece_text = models.TextField(blank=True)


	def __str__(self):
		return self.art_title

	# Overriding the save method so that when an image is deleted or updated,
    #           the old image is deleted from the storage
	def save(self, *args, **kwargs):
		if self.pk:
			old_record = ArticleTitle.objects.get(pk=self.pk)
			if old_record.title_photo != self.title_photo:
				old_record.title_photo.delete(save=False)
		super(ArticleTitle, self).save(*args, **kwargs)

	# adding an imageURL method to exclude an error if the image is missing
	@property
	def imageUrl(self):
		try:
			im = self.title_photo.url
		except:
			im = ''
		return im


class ArticleBody(models.Model):
	art_title = models.ForeignKey(ArticleTitle, on_delete=models.CASCADE, null=True, blank=True)
	art_photo = models.ImageField(upload_to='blog_photo', blank=True)
	art_text = models.TextField(blank=True)	

	def __str__(self):
		name = str(self.art_title) + " " + str(self.id)
		return name

	# Overriding the save method so that when an image is deleted or updated,
    #           the old image is deleted from the storage
	def save(self, *args, **kwargs):
		if self.pk:
			old_record = ArticleBody.objects.get(pk=self.pk)
			if old_record.art_photo != self.art_photo:
				old_record.art_photo.delete(save=False)
		super(ArticleBody, self).save(*args, **kwargs)

 # adding an imageURL method to exclude an error if the image is missing
	@property
	def imageUrl(self):
		try:
			im = self.art_photo.url
		except:
			im = ''
		return im


# >>>>>>>>>>>>> CONTACT <<<<<<<<<<<<

class ContactDescription(models.Model):
	contact_photo = models.ImageField(null=True, blank=True, upload_to='contact_photo')
	contact_title = models.CharField(null=True, blank=True, max_length=50)	
	contact_text = models.TextField(null=True, blank=True)

	def __str__(self):
		return self.contact_title

	# Overriding the save method so that when an image is deleted or updated,
    #           the old image is deleted from the storage
	def save(self, *args, **kwargs):
		if self.pk:
			old_record = ContactDescription.objects.get(pk=self.pk)
			if old_record.contact_photo != self.contact_photo:
				old_record.contact_photo.delete(save=False)
		super(ContactDescription, self).save(*args, **kwargs)

 # adding an imageURL method to exclude an error if the image is missing
	@property
	def imageUrl(self):
		try:
			im = self.contact_photo.url
		except:
			im = ''
		return im


class ContactData(models.Model):
	normal_text = models.CharField(null=True, blank=True, max_length=50)	
	link_label = models.CharField(null=True, blank=True, max_length=55)
	link_address = models.URLField(null=True, blank=True)
	
