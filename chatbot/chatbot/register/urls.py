from django.urls import path
from . import views

app_name = 'register'
urlpatterns = [
    path('user_create/', views.UserCreateView.as_view(), name='user_create'),
    path('user_create/dane', views.UserCreateDaneView.as_view(), name='user_create_dane'),
    path('user_create/complete/<token>/', views.UserCreateCompleteView.as_view(), name='user_create_complete'),
]
