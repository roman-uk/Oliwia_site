from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth.models import User


	
#        Login Form
class LoginForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')


# Change password Form
class UpdatePasswordForm(PasswordChangeForm, SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #  rewrite error message
        self.error_messages['password_incorrect'] = "Twoje stare hasło zostało wprowadzone nieprawidłowo. Proszę wprowadzić ponownie."
        self.error_messages['password_mismatch'] = "Dwa pola hasła nie pasowały"
        self.fields["old_password"].label = "Stare hasło"
        self.fields["new_password1"].label = "Nowe hasło"
        self.fields["new_password2"].label = "Powtórz nowe hasło"


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
		widgets = {
			'title_photo': FileInput(),
		}
		


class ArticleBodyForm(forms.ModelForm):
	# art_photo = forms.FileField(widget=FileInput())	
	class Meta:
		model = ArticleBody
		fields = '__all__'	

		widgets = {
            'art_text': forms.Textarea(attrs={'cols': 80, 'rows': 15}),
            'art_photo': FileInput(),
        }


class AddBodyForm(ArticleBodyForm):
	class Meta:
		model = ArticleBody
		exclude = ("art_title",)


# 			contact
class ContactDescriptionForm(forms.ModelForm):
	contact_text = forms.CharField(widget=forms.Textarea(attrs={'cols': 80, 'rows':15}))
	class Meta:
		model = ContactDescription
		fields = '__all__'


class ContactDataForm(forms.ModelForm):		
	normal_text = forms.CharField(required=False, widget=forms.TextInput(attrs={'size': 50,}))
	link_label = forms.CharField(required=False, widget=forms.TextInput(attrs={'size': 50, 
		'placeholder': 'napis co zobaczą klijenci',}))
	link_address = forms.CharField(required=False, widget=forms.TextInput(attrs={'size': 50, 
		'placeholder': 'adres, do którego link przeprowadzi',}))

	class Meta:
		model = ContactData
		fields = '__all__'


class ClientForm(forms.Form):
	name = forms.CharField(required=False, widget=forms.TextInput(attrs={
		'placeholder': 'Imie',
		'class': 'contact-name'
		}))
	email = forms.EmailField(required=False, widget=forms.TextInput(attrs={
		'placeholder': 'E-mail',
		'class': 'contact-email'
		}))
	subject = forms.CharField(required=False, widget=forms.TextInput(attrs={
		'placeholder': 'Wpisz temat wiadomosci',
		'class': 'contact-subject'
		}))
	message = forms.CharField(widget=forms.Textarea(attrs={
		'cols': 69, 'rows': 15,
		'placeholder': 'Wpisz tresc wiadomosci'
		}))


# the form for specifying (by the owner) the email address to which 
# 			feedback messages from the site will be sent
class MessageForm(forms.Form):	
	email = forms.EmailField()
