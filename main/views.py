from django.shortcuts import render

from django.views.generic import ListView

from main.models import WordCard


# Create your views here.
class WordCardListView(ListView):
    model = WordCard
