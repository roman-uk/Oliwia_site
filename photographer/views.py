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




""" >>>>>>>>>>>> for reusable pages: 'start', 'portrety', 'okolicznosciowe', 
						  'rodzinne', 'sensualne', 'wiecej' 
tab(site_tab) - short page name used for css.style and models
full_name - full name page written bellow the nav-bar <<<<<<<<<<"""


def start_p(request):
	return redirect('reusable_page', tab='start', full_name='Fotograf Bydgoszcz')


# 'start', 'portrety', 'okolicznosciowe', 'rodzinne', 'sensualne', 'wiecej'
def reusable(request, tab='', full_name=''):	
	description = DescriptionReusable.objects.filter(site_tab=tab) #page description		
	filter_foto = request.GET.get('filt', 'all')	
	if filter_foto != 'all' : #------if user clicks filter(theme photo)
		photos = PhotoPortfolio.objects.filter(photo_theme=filter_foto).order_by('seat_number')		
	else:
		photos = PhotoPortfolio.objects.filter(site_tab=tab).order_by('seat_number')						
	columns = ('kolumna1', 'kolumna2', 'kolumna3')
	# getting only the values of the "hoto_theme" field and turning them into a set of unique values
	photo_themes = set(photos.values_list('photo_theme', flat=True)) 
	context = {'photo_themes': photo_themes, "navbar_active": tab, "full_name_tab": full_name, "description": description, 
		"photos": photos, "columns": columns}	
	return render (request, 'photographer/reusable.html', context)
	

# function for adding and editing description on reusable page
def description_reusable(request):
	tab = request.GET.get('tab', '')
	full_name = request.GET.get('full_name', '')	
	if request.method == 'GET': #---if owner clicks add or edit description page
		try:  			#---if clicks edit description page
			descript = DescriptionReusable.objects.get(site_tab=tab)
			description_form = DescriptionReusableForm(initial={'title': descript.title, 'content':descript.content, 'site_tab': tab})
		except:			#---if clicks add description page
			description_form = DescriptionReusableForm(initial={'site_tab': tab})
		context = {'description': description_form, 'tab': tab, 'full_name': full_name}		
		return render(request, 'photographer/description-update.html', context)
	elif request.method == 'POST':
		try:			#	return completed form edit
			descript = DescriptionReusable.objects.get(site_tab=tab)				
			description_form = DescriptionReusableForm(request.POST, instance=descript)
		except:			#	return completed form add
			description_form = DescriptionReusableForm(request.POST)
		if description_form.is_valid():
			description_form.save()			
			return redirect('reusable_page', tab=tab, full_name=full_name)
		else:			
			return HttpResponseNotFound('<h1> Nieprawidłowo wypełnione </h1>')


# function for delete description reusable on page
def delete_description_reusable(request):	
	tab = request.GET.get('tab')
	full_name = request.GET.get('full_name')	
	descript = DescriptionReusable.objects.get(site_tab=tab)
	descript.delete()	
	return redirect('reusable_page', tab=tab, full_name=full_name)


# function for adding photo on reusable page
def add_photo(request):
	tab = request.GET.get('tab')
	full_name = request.GET.get('full_name')	
	if request.method == 'GET':		#	if owner clicks add photo			
		photo = PhotoPortfolioForm(initial={'site_tab': tab})
		context = {'photo': photo, 'tab': tab, 'full_name': full_name}
		return render(request, 'photographer/add-photo.html', context)
	elif request.method == 'POST':	#	return completed form add
		photo = PhotoPortfolioForm(request.POST, request.FILES)		
		if photo.is_valid():			
			photo.save()
			return redirect('reusable_page', tab=tab, full_name=full_name)
		else:
			return HttpResponseNotFound('<h1> Nieprawidłowo wypełnione </h1>')


# function for editing photo on reusable page
def edit_photo(request):
	tab = request.GET.get('tab')
	full_name = request.GET.get('full_name')
	pk = request.GET.get('pk')	
	old= PhotoPortfolio.objects.get(id=pk)
	if request.method == 'GET':		#	if owner clicks edit photo
		# fill the form(photo_form) with existing values
		photo_form = PhotoPortfolioForm(initial={'column': old.column, 'photo': old.photo, 'photo_theme': old.photo_theme, 'seat_number': old.seat_number, 'site_tab': old.site_tab})
		context = {'photo': photo_form, 'tab': tab, 'full_name': full_name, 'id_photo': pk}		
		return render(request, 'photographer/edit-photo.html', context)
	elif request.method == 'POST':		#	return completed form edit
		photo_form = PhotoPortfolioForm(request.POST, request.FILES, instance=old)
		if photo_form.is_valid():
			photo_form.save()
			return redirect('reusable_page', tab=tab, full_name=full_name)
		else:
			return HttpResponseNotFound('<h1> Nieprawidłowo wypełnione </h1>')


# photo deletion function on reusable page
def delete_photo(request):
	tab = request.GET.get('tab')
	full_name = request.GET.get('full_name')
	pk = request.GET.get('pk')
	photo= PhotoPortfolio.objects.get(id=pk)
	photo.delete()
	return redirect('reusable_page', tab=tab, full_name=full_name)


# >>>>>>>>>>>>>>>>> blog page <<<<<<<<<<<<<<<<<
def blog(request, tab='', full_name=''):
	first_article = FirstArticle.objects.all()	
	art_titles = ArticleTitle.objects.order_by('-id')
	art_body = ArticleBody.objects.all()
	context = {"navbar_active": tab, "full_name_tab": full_name, 
		"first_article": first_article, 'art_titles': art_titles, 'art_body': art_body}
	return render(request, 'photographer/blog.html', context)


# adding new articles to the blog page.
def add_article(request):
	tab = request.GET.get('tab')
	full_name = request.GET.get('full_name')
#	--request for a form for adding an article
	if request.method == 'GET': 	
		title = ArticleTitleForm() #	--the form for the article title
		article = ArticleBodyForm() # 	--the form for the article body	without field art_title. field was excluded in Forms
		context = {"navbar_active": tab, "full_name": full_name, 'title': title,
			'article': article}		
		return render (request, 'photographer/blog-add.html', context)
# 	--returning the form for adding an article
	elif request.method == "POST":		
		title = ArticleTitleForm(request.POST)	#	-- saving the article title	
		title.save()
		title = title.cleaned_data
		title = title['art_title']
		title = ArticleTitle.objects.get(art_title=title)		
		# title = title['art_title'].value()
		article = ArticleBodyForm(request.POST, request.FILES)#	--the article body without title(art_title=0).
		article.save() 
		article = article.cleaned_data
		article = article['art_text']		
		article = ArticleBody.objects.get(art_text=article)
		article.art_title = title	# --replacing null article title with the one entered by the user.			
		article.save(update_fields=['art_title'])
		return redirect('blog_page', tab=tab, full_name=full_name)


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

