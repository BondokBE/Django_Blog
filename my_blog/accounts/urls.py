from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path('login', views.user_login, name="login"),
    path('register', views.user_register, name="register"),
    path('logout', views.user_logout, name="logout"),
    path('profile', views.user_profile, name='profile'),
    path('profile_edit', views.profile_edit, name='profile_edit'),
    path('password_change', views.password_change, name='password_change'),
]


