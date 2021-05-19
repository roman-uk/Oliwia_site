from django.shortcuts import render
from .models import *



""" >>>>>>>>>>>> for pages: 'start', 'portrety', 'okolicznosciowe', 
						  'rodzinne', 'sensualne', 'wiecej' <<<<<<<<<<"""
def reusable(request, tab='', active=''):		
	description = DescriptionReusable.objects.filter(site_tab=tab)	
	photo_themes = PhotoTheme.objects.filter(site_tab=tab)
	filter_foto = request.GET.get('filt', 'all')	
	if filter_foto != 'all' :
		photos = PhotoPortfolio.objects.filter(photo_theme=filter_foto).order_by('seat_number')
	else:
		photos = PhotoPortfolio.objects.filter(site_tab=tab).order_by('seat_number')		
	columns = ('kolumna1', 'kolumna2', 'kolumna3')
	context = {"navbar_active": tab, "full_name_tab": active,	"description": description, 
		'photo_themes': photo_themes, "photos": photos, "columns": columns}
	return render (request, 'photographer/reusable.html', context)


# >>>>>>>>>>>>>>>>> blog page <<<<<<<<<<<<<<<<<
def blog(request):
	context = {}
	return render(request, 'photographer/blog.html', context)


# >>>>>>>>>>>>>>>>> kontakt page <<<<<<<<<<<<<<<<<
def contact(request):
	context = {}
	return render(request, 'photographer/kontakt.html', context)

