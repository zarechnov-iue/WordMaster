from django.views.generic import ListView
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages

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

    def post(self, request, *args, **kwargs):
        # Получение данных из POST-запроса
        word = request.POST.get('word')
        translation = request.POST.get('translation')
        illustration = request.POST.get('illustration')

        # Проверка обязательных полей
        if not word or not translation:
            messages.error(request, "Поля 'Слово' и 'Перевод' являются обязательными.")
            return render(request, "add_card.html", {'word': word, 'translation': translation, 'illustration': illustration})

        try:
            # Создание новой карточки слова
            WordCard.objects.create(
                word=word,
                translation=translation,
                image=illustration  # Сохраняем URL иллюстрации
            )
            messages.success(request, "Карточка успешно добавлена!")
            return render(request, "add_card.html")

        except Exception as e:
            # Обработка ошибок при создании карточки
            messages.error(request, f"Ошибка при добавлении карточки: {str(e)}")
            return render(request, "add_card.html", {'word': word, 'translation': translation, 'illustration': illustration})
class CardsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "cards.html")

class StudyView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "study.html")