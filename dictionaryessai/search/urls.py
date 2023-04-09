from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('search', views.search, name='search'),
    path('register', views.register, name='register'),
    path('index', views.index, name='index'),
    path('logout', views.logout, name='logout'),
    path('translatef', views.translatef, name='translatef'),
    path('translate1', views.translate1, name='translate1'),
]
