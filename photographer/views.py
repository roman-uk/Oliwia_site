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
	modal = request.GET.get('modal', "none")
	context = {"navbar_active": tab, "full_name_tab": full_name, 'modal': modal, 
		"first_article": first_article, 'art_titles': art_titles, 'art_body': art_body}
	return render(request, 'photographer/blog.html', context)


# creating or editing an article that is attached to the top of the page
def top_article(request):
	tab = request.GET.get('tab')
	full_name = request.GET.get('full_name')
	pk = request.GET.get('pk', '')	# id of the article is edited
	if request.method == "GET":		
		if pk == '':	#add new article
			article_form = FirstArticleForm()			
		elif pk != '':	#editing exist article
			article = FirstArticle.objects.get(id=pk)
			article_form = FirstArticleForm(initial={'art_photo': article.art_photo,
				'art_title': article.art_title, 'art_text': article.art_text})		
		context = {"navbar_active": tab, "full_name": full_name, 'article_form': article_form, 'pk':pk}
		return render(request, 'photographer/blog-top-article.html', context)
	elif request.method == 'POST':
		try:		#editing the exist article
			old_article = FirstArticle.objects.get(id=pk)
			new_article = FirstArticleForm(request.POST, request.FILES, instance=old_article )
			if new_article.is_valid:
				new_article.save()
			else:
				return HttpResponseNotFound('<h1> Nieprawidłowo wypełnione </h1>')
		except:		#add new article
			article = FirstArticleForm(request.POST, request.FILES)
			if article.is_valid:
				article.save()
			else:
				return HttpResponseNotFound('<h1> Nieprawidłowo wypełnione </h1>')			
		return redirect('blogURL', tab=tab, full_name=full_name)


# delete an article that is attached to the top of the page
def delete_top_article(request):
	tab = request.GET.get('tab')
	full_name = request.GET.get('full_name')
	pk = request.GET.get('pk')	# id of the article is deleted
	article = FirstArticle.objects.get(id=pk)
	article.delete()
	return redirect('blogURL', tab=tab, full_name=full_name)


# adding new articles to the blog page.
def add_article(request):
	tab = request.GET.get('tab')
	full_name = request.GET.get('full_name')
#	--request for a form for adding an article
	if request.method == 'GET': 	
		title = ArticleTitleForm() #	--the form for the article title
		article = AddBodyForm() # 	--the form for the article body	without field art_title. field was excluded in Forms
		context = {"navbar_active": tab, "full_name": full_name, 'title': title,
			'article': article}		
		return render (request, 'photographer/blog-add.html', context)
# 	--returning the form for adding an article
	elif request.method == "POST":		
		title = ArticleTitleForm(request.POST)	#	-- saving the article title	
		title.save()
		title = title.cleaned_data
		title = title['art_title']	#  == title['art_title'].value()
		title = ArticleTitle.objects.get(art_title=title)			
		article = AddBodyForm(request.POST, request.FILES)#	--the article body without title. title=blank.
		article.save()		 #	saving the article body
		article = article.cleaned_data
		article = article['art_text']		
		article = ArticleBody.objects.get(art_text=article)
		article.art_title = title	# --replacing blank article title with the one entered by the user.			
		article.save(update_fields=['art_title'])	#	overwrite only "art_titlt"  field
		return redirect('blogURL', tab=tab, full_name=full_name)


# editing an article
	# this function uses the same template as "expand_article"
def edit_article(request):
	tab = request.GET.get('tab')
	full_name = request.GET.get('full_name')	
	pk= request.GET.get('pk', '') # id 
	field = request.GET.get('field')   # the field that will change (title or image or text)	
	if request.method == 'GET':
		help_text = 'Edytuj wpis na stronie blog '
		if field == 'title':
			title = ArticleTitle.objects.get(id=pk)
			title_form = ArticleTitleForm(initial={'art_title': title.art_title})			
			context = {"navbar_active": tab, "full_name": full_name, 'help_text': help_text, 
				'title_form':title_form, 'field': field, 'pk': pk, 'edit_or_expand':'edit_articleURL'}		
		elif field != 'title':			
			body = ArticleBody.objects.get(id=pk)
			body_form = ArticleBodyForm(initial={'art_title': body.art_title, 'art_photo': body.art_photo,
				'art_text': body.art_text})			
			context = {"navbar_active": tab, "full_name": full_name,  'help_text': help_text,
				'body_form': body_form, 'field': field, 'pk': pk, 'edit_or_expand':'edit_articleURL'}
		return render(request, 'photographer/blog-edit.html', context)
	elif request.method == "POST":
		if field == 'title':
			old_title = ArticleTitle.objects.get(id=pk)
			title = ArticleTitleForm(request.POST, instance=old_title)
			title.save()
		elif field != 'title':
			old_body = ArticleBody.objects.get(id=pk)
			article = ArticleBodyForm(request.POST, request.FILES, instance=old_body)
			article.save()
		return redirect('blogURL', tab=tab, full_name=full_name)


# this function extends an existing article by adding a photo or text.
	# the function uses the same template as "edit_article"
def expand_article(request):
	tab = request.GET.get('tab')
	full_name = request.GET.get('full_name')
	pk= request.GET.get('pk', '')	# id of the foreign key(art_title). article name.
	title = ArticleTitle.objects.get(id=pk)
	if request.method == 'GET':
		body_form = ArticleBodyForm(initial={'art_title': title.id})
		help_text = "Tutaj możesz poszerzyć artykuł i dodać do niego zdjęcie lub tekst."
		context = {"navbar_active": tab, "full_name": full_name, 'body_form': body_form, 'help_text': help_text, 
			'field': 'image, .text', 'pk': pk, 'edit_or_expand':'expand_articleURL'}
		return render(request, 'photographer/blog-edit.html', context)
	elif request.method == 'POST':
		article = ArticleBodyForm(request.POST, request.FILES)
		if article.is_valid:
			article.save()
			return redirect('blogURL', tab=tab, full_name=full_name)
		else:
			return HttpResponseNotFound('<h1> Nieprawidłowo wypełnione </h1>')


# delete part of the article(image or text)
def del_part_article(request):
	tab = request.GET.get('tab')
	full_name = request.GET.get('full_name')
	pk= request.GET.get('pk', '')	# id of the article from which the field will be deleted
	field = request.GET.get('field') # the field that will delete(image or text)
	article = ArticleBody.objects.get(id=pk)
	if field == 'text':					
		article.art_text = ''
		if article.art_photo == '':
			article.delete()
			return redirect('blogURL', tab=tab, full_name=full_name)
	elif field == 'image':
		article.art_photo = ''
		if article.art_text == '':
			article.delete()
			return redirect('blogURL', tab=tab, full_name=full_name)	
	article.save()
	return redirect('blogURL', tab=tab, full_name=full_name)


# delete an article
def delete_article(request):
	tab = request.GET.get('tab')
	full_name = request.GET.get('full_name')
	pk = request.GET.get('pk')	
	article = ArticleTitle.objects.get(id=pk)
	article.delete()
	return redirect('blogURL', tab=tab, full_name=full_name)

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

