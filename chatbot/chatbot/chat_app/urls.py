from django.urls import path
from . import views

app_name = 'chat_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('ajax/', views.ajax_index, name='ajax_index'),
]
