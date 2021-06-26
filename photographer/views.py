from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import *
from .forms import *
from django.views.generic import CreateView, UpdateView
from django.http import HttpResponseNotFound

# h: oliwia 	p: roman

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart




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
	


def description_reusable(request):
	tab = request.GET.get('tab', '')
	full_name = request.GET.get('full_name', '')	
	if request.method == 'GET':
		try:
			descript = DescriptionReusable.objects.get(site_tab=tab)
			description_form = DescriptionReusableForm(initial={'title': descript.title, 'content':descript.content, 'site_tab': tab})
		except:
			description_form = DescriptionReusableForm(initial={'site_tab': tab})
		context = {'description': description_form, 'tab': tab, 'full_name': full_name}		
		return render(request, 'photographer/description-update.html', context)
	elif request.method == 'POST':
		try:
			descript = DescriptionReusable.objects.get(site_tab=tab)				
			description_form = DescriptionReusableForm(request.POST, instance=descript)
		except:
			description_form = DescriptionReusableForm(request.POST)
		if description_form.is_valid():
			description_form.save()			
			return redirect('reusable_page', tab=tab, full_name=full_name)
		else:			
			return HttpResponseNotFound('<h1> Nieprawidłowo wypełnione </h1>')


def delete_description_reusable(request):	
	tab = request.GET.get('tab')
	full_name = request.GET.get('full_name')	
	descript = DescriptionReusable.objects.get(site_tab=tab)
	descript.delete()	
	return redirect('reusable_page', tab=tab, full_name=full_name)

# =======================================
def photo_theme(request):
	tab = request.GET.get('tab')
	full_name = request.GET.get('full_name')
	item = request.GET.get('item', '')
	if request.method == 'GET':
		try:			
			theme = PhotoTheme.objects.get(photo_theme=item)
			theme = PhotoThemeForm(initial={'site_tab': tab, 'photo_theme': theme.photo_theme})
			context = {'theme': theme, 'tab': tab, 'full_name': full_name, 'item': item}			
		except:
			theme = PhotoThemeForm(initial={'site_tab': tab})
			context = {'theme': theme, 'tab': tab, 'full_name': full_name, 'item': item}
		return render(request, 'photographer/photo-theme.html', context)
	elif request.method == 'POST':
		try:
			old_theme = PhotoTheme.objects.get(photo_theme=item)
			theme_form = PhotoThemeForm(request.POST, instance=old_theme)
			if theme_form.is_valid():
				theme_form.save()				
				return redirect('reusable_page', tab=tab, full_name=full_name)
			else:
				return HttpResponseNotFound('<h1> Nieprawidłowo wypełnione </h1>')
		except:
			theme = PhotoThemeForm(request.POST)
			if theme.is_valid():
				theme.save()
				return redirect('reusable_page', tab=tab, full_name=full_name)
			else:
				return HttpResponseNotFound('<h1> Nieprawidłowo wypełnione </h1>')


def delete_photo_theme(request):
	tab = request.GET.get('tab')
	full_name = request.GET.get('full_name')
	item = request.GET.get('item')
	item = PhotoTheme.objects.get(photo_theme=item)
	item.delete()
	return redirect('reusable_page', tab=tab, full_name=full_name)


def add_photo(request):
	tab = request.GET.get('tab')
	full_name = request.GET.get('full_name')
	
	# print('---------------', theme)
	if request.method == 'GET':	
			
		photo = PhotoPortfolioForm(initial={'site_tab': tab})
		context = {'photo': photo, 'tab': tab, 'full_name': full_name}
		return render(request, 'photographer/add-photo.html', context)
	elif request.method == 'POST' :
		photo = PhotoPortfolioForm(request.POST, request.FILES)		
		if photo.is_valid():			
			photo.save()
			return redirect('reusable_page', tab=tab, full_name=full_name)
		else:
			return HttpResponseNotFound('<h1> Nieprawidłowo wypełnione </h1>')



	# pk = request.GET.get('pk', '')
	# photo = PhotoPortfolio.objects.get(id=pk)


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
	contact_descript = ContactDescription.objects.all()
	contact_data = ContactData.objects.all()
	client_form = ClientForm()
	context = {"navbar_active": 'contact', 'contact_descript': contact_descript,
		'contact_data': contact_data, 'client_form': client_form}
	if request.method == 'POST':
		msg = MIMEMultipart()
		message = request.POST.get('message')
		from_email = 'Od:' + ' ' + request.POST.get('name')	
		html = '<html><head><h2>' + from_email + '</h2></head><body><p>' + message + '</p></body></html>'
		to_email = 'korbex21@gmail.com'			
		msg['Subject'] = request.POST.get('subject')		
		msg['To'] = request.POST.get('email')			
		msg.attach(MIMEText(html, 'html'))
		server = smtplib.SMTP('smtp.gmail.com: 587')
		server.starttls()
		server.login('korbex21@gmail.com', 'J(ek*NyV$fc)Mi3brKJS')
		server.sendmail(from_email, to_email, msg.as_string())
		server.quit()
		return redirect('contact_page')
	return render(request, 'photographer/kontakt.html', context)

