from django.urls import path
from . import views

app_name = 'posts'  # this is the namespace of the app

urlpatterns = [
    path('', views.post_list, name='base'),
    path('post/<slug:slug>/', views.post_details, name='post'),
    path('post_create/', views.post_create, name='post_create'),
    path('edit/<slug:slug>/', views.post_edit, name='edit'),
    path('delete/<slug:slug>/', views.post_delete, name='delete'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact')
]


