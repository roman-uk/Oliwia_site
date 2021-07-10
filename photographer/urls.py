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
	path('blog/<str:tab>/<str:full_name>', views.blog, name='blogURL'),
	path('blog/add-article', views.add_article, name='add_articleURL'),
	path('blog/edit-article', views.edit_article, name='edit_articleURL'),
	path('blog/expand-article', views.expand_article, name='expand_articleURL'),
	path('blog/delete-article', views.delete_article, name='delete_articleURL'),
	path('blog/delete-part-article', views.del_part_article, name='del_part_articleURL'),
	path('blog/top-article', views.top_article, name='top_articleURL'),
	path('blog/delete-top-article', views.delete_top_article, name='delete_top_articleURL'),
	path('contact', views.contact, name='contact_page'),			
]
