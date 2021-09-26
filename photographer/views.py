from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import *
from .forms import *
from django.views.generic import CreateView, UpdateView, DeleteView
from django.http import HttpResponseNotFound, HttpResponse
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from .config_email import *
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages


#  >>>>>>>>>>>>>>>> LOGIN<<<<<<<<<<<<<<<
#   Login/Logout
class ServiceLogin(LoginView):
    template_name = 'photographer/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('start_page')

    def get_success_url(self):
        return self.success_url


class ServiceLogout(LogoutView):
    next_page = reverse_lazy('start_page')


# Change password
class UpdatePassword(LoginRequiredMixin, PasswordChangeView):
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('start_page')
    template_name = 'photographer/change-password.html'


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
@login_required(login_url=reverse_lazy('loginURL')) # Verifying user authorization
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
@login_required(login_url=reverse_lazy('loginURL')) # Verifying user authorization
def delete_description_reusable(request):	
	tab = request.GET.get('tab')
	full_name = request.GET.get('full_name')	
	descript = DescriptionReusable.objects.get(site_tab=tab)
	descript.delete()	
	return redirect('reusable_page', tab=tab, full_name=full_name)


# function for adding photo on reusable page
@login_required(login_url=reverse_lazy('loginURL')) # Verifying user authorization
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
@login_required(login_url=reverse_lazy('loginURL')) # Verifying user authorization
def edit_photo(request):
	tab = request.GET.get('tab')
	full_name = request.GET.get('full_name')
	pk = request.GET.get('pk')	
	old= PhotoPortfolio.objects.get(id=pk)
	if request.method == 'GET':		#	if owner clicks edit photo
		# fill the form(photo_form) with existing values
		photo_form = PhotoPortfolioForm(initial={'column': old.column, 'photo': old.photo, 
			'photo_theme': old.photo_theme, 'seat_number': old.seat_number, 'site_tab': old.site_tab})
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
@login_required(login_url=reverse_lazy('loginURL')) # Verifying user authorization
def delete_photo(request):
	tab = request.GET.get('tab')
	full_name = request.GET.get('full_name')
	pk = request.GET.get('pk')
	photo= PhotoPortfolio.objects.get(id=pk)
	photo.delete()
	return redirect('reusable_page', tab=tab, full_name=full_name)


# >>>>>>>>>>>>>>>>> BLOG PAGE <<<<<<<<<<<<<<<<<
def blog(request):
	first_article = FirstArticle.objects.all()	
	art_titles = ArticleTitle.objects.order_by('-id')	
	context = {"first_article": first_article, 'art_titles': art_titles}
	return render(request, 'photographer/blog.html', context)


def blog_item(request):
	pk = request.GET.get('pk')
	title = ArticleTitle.objects.get(id=pk)	
	article = ArticleBody.objects.filter(art_title=pk)
	context = {'article': article, 'title': title}	
	return render(request, 'photographer/blog-item.html', context)


# creating or editing an article that is attached to the top of the page
@login_required(login_url=reverse_lazy('loginURL')) # Verifying user authorization
def top_article(request):	
	pk = request.GET.get('pk', '')	# id of the article is edited
	if request.method == "GET":		
		if pk == '':	#add new article
			article_form = FirstArticleForm()			
		elif pk != '':	#editing exist article
			article = FirstArticle.objects.get(id=pk)
			article_form = FirstArticleForm(initial={'art_photo': article.art_photo,
				'art_title': article.art_title, 'art_text': article.art_text})		
		context = {'article_form': article_form, 'pk':pk}
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
		return redirect('blogURL')


# delete an article that is attached to the top of the page
@login_required(login_url=reverse_lazy('loginURL')) # Verifying user authorization
def delete_top_article(request):
	pk = request.GET.get('pk')	# id of the article is deleted
	article = FirstArticle.objects.get(id=pk)
	article.delete()
	return redirect('blogURL')


# adding new articles to the blog page.
@login_required(login_url=reverse_lazy('loginURL')) # Verifying user authorization
def add_article(request):
#	--request for a form for adding an article
	if request.method == 'GET': 	
		title = ArticleTitleForm() #	--the form for the article title
		article = AddBodyForm() # 	--the form for the article body	without field art_title. field was excluded in Forms
		context = {'title': title, 'article': article}		
		return render (request, 'photographer/blog-add.html', context)
# 	--returning the form for adding an article
	elif request.method == "POST":		
		title = ArticleTitleForm(request.POST, request.FILES)	#	-- saving the article title	
		title.save()
		title = title.cleaned_data
		title = title['art_title']	#  == title['art_title'].value()
		title = ArticleTitle.objects.get(art_title=title)			
		article = AddBodyForm(request.POST, request.FILES)#	--the article body without title. title=blank.
		art_text = article['art_text'].value()
		art_photo = article['art_photo'].value()
		if art_text != '':
			article.save() #	--the article body without title. title=blank.
			article = ArticleBody.objects.get(art_text=art_text)
			article.art_title = title	# --replacing blank article title with the one entered by the user.			
			article.save(update_fields=['art_title']) #	overwrite only "art_titlt"  field
		elif art_photo != None:
			article.save() #	--the article body without title. title=blank.
			article = ArticleBody.objects.get(art_photo=article['art_photo'])
			article.art_title = title	# --replacing blank article title with the one entered by the user.			
			article.save(update_fields=['art_title']) #	overwrite only "art_titlt"  field
		return redirect('blogURL')


# editing an article
	# this function uses the same template as "expand_article"
@login_required(login_url=reverse_lazy('loginURL')) # Verifying user authorization
def edit_article(request):	
	pk= request.GET.get('pk', '') # id 	
	field = request.GET.get('field')   # the field that will change (title or image or text)	
	if request.method == 'GET':
		help_text = 'Edytuj wpis na wkładce BLOG '
		if field == 'title':
			title = ArticleTitle.objects.get(id=pk)
			title_form = ArticleTitleForm(initial={'art_title': title.art_title,
				'title_font': title.title_font, 'title_photo': title.title_photo,
				'piece_text': title.piece_text})			
			context = {'help_text': help_text, 'title_form':title_form, 
				'field': field, 'pk': pk, 'edit_or_expand':'edit_articleURL'}		
		elif field != 'title':			
			body = ArticleBody.objects.get(id=pk)
			body_form = ArticleBodyForm(initial={'art_title': body.art_title, 'art_photo': body.art_photo,
				'art_text': body.art_text})			
			context = {'help_text': help_text, 'body_form': body_form, 'field': field, 
				'pk': pk, 'edit_or_expand':'edit_articleURL'}
		return render(request, 'photographer/blog-edit.html', context)
	elif request.method == "POST":
		if field == 'title':
			old_title = ArticleTitle.objects.get(id=pk)
			title = ArticleTitleForm(request.POST, request.FILES, instance=old_title)
			title.save()
		elif field != 'title':
			old_body = ArticleBody.objects.get(id=pk)
			article = ArticleBodyForm(request.POST, request.FILES, instance=old_body)
			article.save()
		return redirect('blogURL')


# this function extends an existing article by adding a photo or text.
	# the function uses the same template as "edit_article"
@login_required(login_url=reverse_lazy('loginURL')) # Verifying user authorization
def expand_article(request):
	pk= request.GET.get('pk', '')	# id of the foreign key(art_title). article name.
	title = ArticleTitle.objects.get(id=pk)
	if request.method == 'GET':
		body_form = ArticleBodyForm(initial={'art_title': title.id})
		help_text = "Tutaj możesz poszerzyć artykuł i dodać do niego zdjęcie lub tekst."
		context = {'body_form': body_form, 'help_text': help_text, 
			'field': 'image, .text', 'pk': pk, 'edit_or_expand':'expand_articleURL'}
		return render(request, 'photographer/blog-edit.html', context)
	elif request.method == 'POST':
		article = ArticleBodyForm(request.POST, request.FILES)
		if article.is_valid:
			article.save()
			return redirect('blogURL')
		else:
			return HttpResponseNotFound('<h1> Nieprawidłowo wypełnione </h1>')


# delete part of the article(image or text)
@login_required(login_url=reverse_lazy('loginURL')) # Verifying user authorization
def del_part_article(request):
	pk= request.GET.get('pk', '')	# id of the article from which the field will be deleted
	field = request.GET.get('field') # the field that will delete(image or text)
	article = ArticleBody.objects.get(id=pk)
	if field == 'text':					
		article.art_text = ''
		if article.art_photo == '':
			article.delete()
			return redirect('blogURL')
	elif field == 'image':
		article.art_photo = ''
		if article.art_text == '':
			article.delete()
			return redirect('blogURL')	
	return redirect('blogURL')


# deliting the entire article
@login_required(login_url=reverse_lazy('loginURL')) # Verifying user authorization
def delete_article(request):
	pk = request.GET.get('pk')	
	article = ArticleTitle.objects.get(id=pk)
	article.delete()
	return redirect('blogURL')
	

# >>>>>>>>>>>>>>>>> kontakt page <<<<<<<<<<<<<<<<<

# render contact page
def contact(request):	
	contact_descript = ContactDescription.objects.all()	
	contact_data = ContactData.objects.all()
	client_form = ClientForm()
	message_form = MessageForm()
	context = {'contact_descript': contact_descript,
		'contact_data': contact_data, 'client_form': client_form, 'message_form': message_form}	
		# submit message from contact form to owner site's email 
	if request.method == 'POST':
		try:
			# receiver_message.json -file with owner site's email 
			# message - message sent from the contact form 
			# server - email which sends message to owner's site email
			# importing the login and password from another file
			with open('receiver_message.json', 'r') as email: 
				receiver = json.load(email)
				email.close()
			message = request.POST.get('message')
			subject = request.POST.get('subject')
			from_email = 'Od:' + ' ' + request.POST.get('name')
			to_answer = request.POST.get('email')
			msg = MIMEMultipart()
			msg['From'] = login
			msg['To'] = receiver		
			msg.add_header('reply-to', to_answer)			
			server = smtplib.SMTP_SSL('smtp.rambler.ru: 465')
			server.login(login, password)		
			html_body = '<html><head><h2>' + from_email + '</h2></head><body><p>' \
				+ message + '</p>\n\n Zwrotny adress: '+' &ensp; ' + to_answer+ '</body></html> '
			msg = MIMEText(html_body, 'html', 'utf-8')
			msg['Subject'] = Header(subject, 'utf-8')		
			server.sendmail(login, receiver, msg.as_string())		
			server.quit()
			done = '<hmml><body><h1>Twoja wiadomość została wysłana.</h1>\n \
				<h2><a href=%s>Powrót</h2></body></html>' % reverse_lazy('contactURL')
			return HttpResponse(done)
		# if isn't possible to do this 
		except:
			return HttpResponseNotFound('<h1> Coś poszło nie tak,\
			 spróbuj ponownie lub użyj innego sposobu, aby się ze mną skontaktować </h1>')	
	return render(request, 'photographer/kontakt.html', context)


# create a description or additional information at the top of the page
class CreateDescription(LoginRequiredMixin, CreateView):
	model = ContactDescription
	form_class = ContactDescriptionForm
	template_name = 'photographer/contact-description.html'	
	success_url = reverse_lazy('contactURL')


# edit a description at the top of the page
class EditDescription(LoginRequiredMixin, UpdateView):
	model = ContactDescription
	form_class = ContactDescriptionForm	
	template_name = 'photographer/contact-description.html'
	success_url = reverse_lazy('contactURL')


# delete a description at the top of the page
class DeleteDescription(LoginRequiredMixin, DeleteView):
    model = ContactDescription
    success_url = reverse_lazy('contactURL')

    # I'm overriding the get() method to disable coonfirmation of deleting
    def get(self, request, *args, **kwargs):	 
        return self.post(request, *args, **kwargs)


# creating or editing the contact information such as: telphone, email, facebook etc.
@login_required(login_url=reverse_lazy('loginURL')) # Verifying user authorization
def contact_data(request):
	pk= request.GET.get('pk', '')     # id of the contact data to edit
	field = request.GET.get('field')  # the field that will be change
	if request.method == 'GET':
		try:			
				# submit a form for editing a contact details
			data = ContactData.objects.get(id=pk)
			form = ContactDataForm(initial={'normal_text': data.normal_text, 
				'link_label': data.link_label, 'link_address': data.link_address})						
		except:	
				# submit a form for adding new contact details		
			form = ContactDataForm()
		context = {'form': form, 'field': field, 'pk': pk}
		return render(request, 'photographer/contact-data.html', context)
	if request.method == 'POST':
		try:
				#try edit contact details
			old_data = ContactData.objects.get(id=pk)
			data = ContactDataForm(request.POST, instance=old_data)
		except:
				# add new contact details
			data = ContactDataForm(request.POST)
		if data.is_valid:
			data.save()
		else:
			return HttpResponseNotFound('<h1> Nieprawidłowo wypełnione </h1>')
		return redirect('contactURL')


# delete the contact information 
@login_required(login_url=reverse_lazy('loginURL')) # Verifying user authorization
def delete_contact_data(request):
	pk= request.GET.get('pk')	# id of the contact data to delete
	data = ContactData.objects.get(id=pk)
	data.delete()
	return redirect('contactURL')


# email address for receiving messages from a completed form on the site.
@login_required(login_url=reverse_lazy('loginURL')) # Verifying user authorization
def receiver_message(request):
	receiver = request.POST.get('email')	
	with open('receiver_message.json', 'w') as email:
		json.dump(receiver, email)
		email.close()
	return redirect('contactURL')
