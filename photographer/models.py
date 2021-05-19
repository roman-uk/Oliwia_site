from django.db import models


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


# 	The model for filtering photos on a page by topic.
class PhotoTheme(models.Model):
	photo_theme = models.CharField(max_length=50, unique=True)
	site_tab = models.CharField(max_length=20, choices=site_tabs)


	def __str__(self):
		return self.photo_theme


#	The model for the page description and additional information for customers.
class DescriptionReusable(models.Model):
	title = models.CharField(max_length=50, null=True, blank=True)
	content = models.TextField(null=True, blank=True)
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
	photo = models.ImageField(upload_to='reusable_photo')
	photo_theme = models.ForeignKey(PhotoTheme, null=True, 
		blank=True, on_delete=models.PROTECT)
	column = models.CharField(max_length=20, choices=columns)
	seat_number = models.CharField(max_length=40) # the place of the photo in the column.
	site_tab = models.CharField(max_length=30, choices=site_tabs)


	def __str__(self):
		name = self.site_tab + ' ' + self.photo.name[15:]
		return name
