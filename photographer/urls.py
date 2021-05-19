from django.urls import path
from photographer import views


urlpatterns = [	
	path('reusable/<str:tab>/<str:active>', views.reusable, name='reusable_page'),	
	path('blog', views.blog, name='blog_page'),
	path('kontakt', views.contact, name='kontakt_page'),		
]
