"""
URL configuration for WordMaster project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from main import views

urlpatterns = [
    path('', views.IndexView.as_view(),  name='index'),
    path('add-card', views.AddCardView.as_view(),  name='add-card'),
    path('cards', views.CardsView.as_view(),  name='cards'),
    path('study', views.StudyView.as_view(),  name='study'),
    path('delete-card/<int:card_id>/',  views.DeleteCardView.as_view(), name='delete-card'),
]

urlpatterns += static('images', document_root=settings.MEDIA_ROOT+'/images')