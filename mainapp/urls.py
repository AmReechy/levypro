from django.urls import path
from . import views

app_name = 'mainapp'

urlpatterns = [
    path('', views.index, name='index'),
    #path('contact/', views.contact, name='contact'),
    #path('<int:post_id>/', views.detail, name='detail'), # Captures a dynamic integer parameter
]

