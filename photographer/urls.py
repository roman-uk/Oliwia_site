from django.urls import path
from photographer import views


urlpatterns = [	
	path('reusable/<str:tab>/<str:full_name>', views.reusable, name='reusable_page'),	
	path('reusable/description', views.description_reusable, name='description_reusable'),
	path('reusable/description-delete', views.delete_description_reusable, name='delete_description_reusable_page'),
	path('reusable/theme-photo', views.photo_theme, name='photo_theme_page'),	
	path('reusable/delete-theme', views.delete_photo_theme, name='delete_photo_theme_page'),
	path('reusable/add-photo', views.add_photo, name='add_photo_page'),
	path('blog/<str:tab>/<str:full_name>', views.blog, name='blog_page'),
	path('contact', views.contact, name='contact_page'),
			
]
