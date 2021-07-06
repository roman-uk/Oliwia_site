from django.urls import path
from photographer import views


urlpatterns = [	
	path('', views.start_p, name='start_page'),
	path('reusable/<str:tab>/<str:full_name>', views.reusable, name='reusable_page'),	
	path('reusable/description', views.description_reusable, name='description_reusable'),
	path('reusable/description-delete', views.delete_description_reusable, name='delete_description_reusable_page'),
	path('reusable/add-photo', views.add_photo, name='add_photo_page'),
	path('reusable/edit_photo', views.edit_photo, name='edit_photo_page'),
	path('reusable/delete_photo', views.delete_photo, name='delete_photo_page'),
	path('blog/<str:tab>/<str:full_name>', views.blog, name='blog_page'),
	path('blog/add-article', views.add_article, name='add_article_page'),
	path('contact', views.contact, name='contact_page'),
			
]
