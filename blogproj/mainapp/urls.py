from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>/', views.post, name='post'),
    path('', views.index, name='index'),

]