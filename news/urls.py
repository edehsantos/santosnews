from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('category/<slug>/', views.Category_list.as_view(), name='category_details'),
    path('<int:id>/<slug>/<int:year>/<int:month>/<int:day>/', views.post_details, name='post_details'),
    path('authors/<str:username>/', views.Post_authors.as_view(), name='post_authors'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('search/', views.post_search, name='post_search'),
    path('contact/', views.contact_us, name='contact'),
    path('about/', views.about_us, name='about_us'),

]
