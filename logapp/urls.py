from django.urls import path
from django.contrib.auth import views as auth_views
from news import views

app_name='logapp'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='logapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]