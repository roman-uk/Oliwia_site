from django import forms
from .models import *


		# reusable
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
		widgets = {
            'art_text': forms.Textarea(attrs={'cols': 80, 'rows': 15}),
        }


			# blog
class ArticleTitleForm(forms.ModelForm):
	class Meta:
		model = ArticleTitle
		fields = '__all__'


class ArticleBodyForm(forms.ModelForm):
	class Meta:
		model = ArticleBody
		fields = '__all__'		
		widgets = {
            'art_text': forms.Textarea(attrs={'cols': 80, 'rows': 15}),
        }


class AddBodyForm(ArticleBodyForm):
	class Meta:
		model = ArticleBody
		exclude = ("art_title",)


# 			contact
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



