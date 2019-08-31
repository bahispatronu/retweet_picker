from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('result', views.result, name='result'),
    path('how', views.howto, name="how"),
    path('about', views.about, name="about")
]