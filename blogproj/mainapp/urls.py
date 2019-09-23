from django.urls import path
from . import views

urlpatterns = [
    path('post/<int:id>', views.post, name='post'),
    path('tag/<str:name>', views.tag, name='tag'),
    path('', views.index, name='index'),

]