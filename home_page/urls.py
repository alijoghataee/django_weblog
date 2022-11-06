from django.urls import path

from . import views


urlpatterns = [
    path('', views.home_page_view, name='home'),
    path('contact_us/', views.contact_us_view, name='contact_us'),
]
