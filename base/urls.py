from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('about/', views.about, name="about"),
    path('sorts/', views.sorts, name="sorts"),
    path('grow/', views.grow, name="how-we-grow"),
    path('facts/', views.facts, name="faq"),
    path('pickup/', views.pickup, name="pickup"),
    path('collection/', views.collection, name="self-collection"),
    path('delivery', views.delivery, name="delivery"),
    path('load_amount/', views.load_amount, name="load_amount"),
    path('adoption/', views.adoption, name="peach-adoption"),
    path('photographers/', views.photographers, name="photographers"),
    path('contacts/', views.contacts, name="contacts"),
]