from django.views.generic import ListView
from django.views import View
from django.shortcuts import render

from main.models import WordCard


# Create your views here.
class WordCardListView(ListView):
    model = WordCard

class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "index.html")

class AddCardView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "add_card.html")

class CardsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "cards.html")

class StudyView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "study.html")