from django.urls import path
from photographer import views


urlpatterns = [
	path('', views.start, name='start_page'),
	path('portrety', views.portrait, name='portrety_page'),
	path('okolicznosciowe', views.events, name='okolicznosciowe_page'),
	path('rodzinne', views.family, name='rodzinne_page'),
	path('sensualne', views.sensuous, name='sensualne_page'),
	path('wiecej', views.more, name='wiecej_page'),
	path('kontakt', views.contact, name='kontakt_page'),

	path('wieczor', views.wieczor, name='wieczor_page'),
	path('chrzest', views.chrzest, name='chrzest_page'),
	path('slub', views.slub, name='slub_page')	
]
