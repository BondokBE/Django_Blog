from django.urls import path
from . import views

app_name = 'comments'  # this is the namespace of the app

urlpatterns = [
    path('thread/<int:id>/', views.comment_thread, name='thread'),
    path('thread/<int:id>/delete/', views.comment_delete, name='delete'),
]
