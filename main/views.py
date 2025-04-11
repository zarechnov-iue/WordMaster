import uuid

from django.views.generic import ListView
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.files.base import ContentFile

import requests
from PIL import Image
from io import BytesIO

from .models import WordCard, ImageModel


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
                image=self.download_image(illustration)
            )
            messages.success(request, "Карточка успешно добавлена!")
            return render(request, "add_card.html")

        except Exception as e:
            # Обработка ошибок при создании карточки
            messages.error(request, f"Ошибка при добавлении карточки: {str(e)}")
            return render(request, "add_card.html", {'word': word, 'translation': translation, 'illustration': illustration})

    def download_image(self, illustration):
        if not illustration:
            print("URL изображения отсутствует.")
            return None

        try:
            # Отправляем GET-запрос
            with requests.get(illustration, stream=True) as response:
                response.raise_for_status()  # Проверяем успешность запроса

                # Преобразуем содержимое ответа в файловый объект
                image_data = BytesIO(response.content)

                # Открываем изображение с помощью PIL
                image = Image.open(image_data)

                # Определяем формат изображения
                image_format = image.format.lower() if image.format else 'jpeg'
                if image_format not in ['jpeg', 'png', 'gif']:
                    print(f"Неподдерживаемый формат изображения: {image_format}")
                    return None

                # Создаем временный файловый объект
                temp_file = BytesIO()
                image.save(temp_file, format=image.format)
                temp_file.seek(0)

                # Создаем экземпляр модели ImageModel
                image_model = ImageModel()
                image_model.uuid = str(uuid.uuid4())
                image_model.data.save(
                    f"{image_model.uuid}.{image_format}",  # Имя файла
                    ContentFile(temp_file.getvalue()),  # Содержимое файла
                    save=True  # Сохраняем объект
                )

                return image_model

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при загрузке изображения: {e}")
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")

        return None
class CardsView(ListView):
    model = WordCard  # Указываем модель, с которой будем работать
    template_name = "cards.html"  # Указываем шаблон для отображения
    context_object_name = "cards"  # Имя переменной, которая будет содержать список карточек в шаблоне
    ordering = ['-created_at']  # Сортировка по дате создания (новые карточки сверху)

class StudyView(View):
    def get(self, request, *args, **kwargs):
        # Получаем ID текущей карточки из параметров запроса (если есть)
        current_card_id = request.GET.get('card_id')

        # Получаем все карточки, отсортированные по дате создания
        cards = WordCard.objects.all().order_by('created_at')

        # Определяем текущую карточку
        if current_card_id:
            current_card = get_object_or_404(WordCard, id=current_card_id)
        else:
            # Если ID не указан, берем первую карточку
            current_card = cards.first()

        if not current_card:
            # Если карточек нет, возвращаем пустой шаблон
            return render(request, "study.html", {'current_card': None})

        # Находим индекс текущей карточки в списке
        card_list = list(cards)
        current_index = card_list.index(current_card)

        # Определяем предыдущую и следующую карточки
        prev_card = card_list[current_index - 1] if current_index > 0 else None
        next_card = card_list[current_index + 1] if current_index < len(card_list) - 1 else None

        # Передаем данные в шаблон
        context = {
            'current_card': current_card,
            'prev_card': prev_card,
            'next_card': next_card,
        }
        return render(request, "study.html", context)


class DeleteCardView(View):
    def post(self, request, card_id, *args, **kwargs):
        card = get_object_or_404(WordCard, id=card_id)
        card.delete()
        messages.success(request, f"Карточка '{card.word}' успешно удалена.")
        return redirect('cards')