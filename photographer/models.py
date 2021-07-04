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
	photo_theme = models.CharField(max_length=50, blank=True, null=True, help_text='Morze być puste')	
	column = models.CharField(max_length=20, choices=columns)
	seat_number = models.CharField(max_length=40) # the place of the photo in the column.
	site_tab = models.CharField(max_length=30, choices=site_tabs)


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

 # adding an imageURL method to exclude an error if the image is missing
	@property
	def imageUrl(self):
		try:
			im = self.art_photo.url
		except:
			im = ''
		return im


class ArticleTitle(models.Model):
	art_title = models.CharField(max_length=50)

	def __str__(self):
		return self.art_title


class ArticleBody(models.Model):
	art_title = models.ForeignKey(ArticleTitle,	on_delete=models.CASCADE)
	art_photo = models.ImageField(upload_to='blog_photo', null=True, blank=True)
	art_text = models.TextField(null=True, blank=True)
	art_order = models.IntegerField()

	def __str__(self):
		name = str(self.art_title) + " " + str(self.art_order)
		return name

 # adding an imageURL method to exclude an error if the image is missing
	@property
	def imageUrl(self):
		try:
			im = self.art_photo.url
		except:
			im = ''
		return im



class ContactDescription(models.Model):
	contact_photo = models.ImageField(null=True, blank=True, upload_to='contact_photo')
	contact_title = models.CharField(null=True, blank=True, max_length=50)	
	contact_text = models.TextField(null=True, blank=True)

	def __str__(self):
		return self.contact_title

 # adding an imageURL method to exclude an error if the image is missing
	@property
	def imageUrl(self):
		try:
			im = self.contact_photo.url
		except:
			im = ''
		return im


class ContactData(models.Model):
	telephone = models.CharField(null=True, blank=True, max_length=15)
	email = models.EmailField(max_length=50, null=True, blank=True)
	facebook_name = models.CharField(null=True, blank=True, max_length=55)
	facebook_link = models.URLField(null=True, blank=True)
	instagram_name = models.CharField(null=True, blank=True, max_length=55)
	instagram_link = models.URLField(null=True, blank=True)

	def __str__(self):
		return self.email
