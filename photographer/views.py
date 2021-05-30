from django.shortcuts import render
from .models import *
# h: oliwia 	p: roman



""" >>>>>>>>>>>> for pages: 'start', 'portrety', 'okolicznosciowe', 
						  'rodzinne', 'sensualne', 'wiecej' <<<<<<<<<<"""
def reusable(request, tab='', full_name=''):		
	description = DescriptionReusable.objects.filter(site_tab=tab)	
	photo_themes = PhotoTheme.objects.filter(site_tab=tab)
	filter_foto = request.GET.get('filt', 'all')	
	if filter_foto != 'all' :
		photos = PhotoPortfolio.objects.filter(photo_theme=filter_foto).order_by('seat_number')
	else:
		photos = PhotoPortfolio.objects.filter(site_tab=tab).order_by('seat_number')		
	columns = ('kolumna1', 'kolumna2', 'kolumna3')
	context = {"navbar_active": tab, "full_name_tab": full_name,	"description": description, 
		'photo_themes': photo_themes, "photos": photos, "columns": columns}
	return render (request, 'photographer/reusable.html', context)


# >>>>>>>>>>>>>>>>> blog page <<<<<<<<<<<<<<<<<
def blog(request, tab='', full_name=''):
	first_article = FirstArticle.objects.all()	
	art_titles = ArticleTitle.objects.order_by('-id')
	art_body = ArticleBody.objects.all()
	context = {"navbar_active": tab, "full_name_tab": full_name, 
		"first_article": first_article, 'art_titles': art_titles, 'art_body': art_body}
	return render(request, 'photographer/blog.html', context)


# >>>>>>>>>>>>>>>>> kontakt page <<<<<<<<<<<<<<<<<
def contact(request):
	context = {}
	return render(request, 'photographer/kontakt.html', context)


# def blog(request, tab, full_name):
# 	context = {}
# 	return render(request, 'photographer/blogg.html', context)