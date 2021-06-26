from django import forms
from .models import *


class PhotoThemeForm(forms.ModelForm):
	class Meta:
		model = PhotoTheme
		fields = ['photo_theme', 'site_tab']


class DescriptionReusableForm(forms.ModelForm):
	class Meta:
		model = DescriptionReusable
		fields = ['title', 'content', 'site_tab']
		widgets = {
		'title': forms.TextInput(attrs={
			'placeholder': 'Tytuł artykułu',
            'style': 'width: 300px',
			}),
            'content': forms.Textarea(attrs={
                'cols': 80, 'rows': 10,
                'placeholder': 'Treść artykułu',
                'style': 'font-size: 14px'
            })
		}


class PhotoPortfolioForm(forms.ModelForm):
	class Meta:
		model = PhotoPortfolio
		fields = ['photo', 'photo_theme', 'column', 'seat_number', 'site_tab']

class FirstArticleForm(forms.ModelForm):
	class Meta:
		model = FirstArticle
		fields = '__all__'


class ArticleBodyForm(forms.ModelForm):
	class Meta:
		model = ArticleBody
		fields = '__all__'



class ContactDescriptionForm(forms.ModelForm):
	class Meta:
		model = ContactDescription
		fields = '__all__'


class ContactDataForm(forms.ModelForm):
	class Meta:
		model = ContactData
		fields = '__all__'


class ClientForm(forms.Form):
	name = forms.CharField(widget=forms.TextInput(attrs={
		'placeholder': 'Imie',
		'class': 'contact-name'
		}))
	email = forms.EmailField(widget=forms.TextInput(attrs={
		'placeholder': 'E-mail',
		'class': 'contact-email'
		}))
	subject = forms.CharField(widget=forms.TextInput(attrs={
		'placeholder': 'Wpisz temat wiadomosci',
		'class': 'contact-subject'
		}))
	message = forms.CharField(widget=forms.Textarea(attrs={
		'cols': 69, 'rows': 15,
		'placeholder': 'Wpisz tresc wiadomosci'
		}))



