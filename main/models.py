from django.db import models

class ImageModel(models.Model):
    uuid = models.CharField(max_length=100)
    data = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.uuid

class WordCard(models.Model):
    # Поле для хранения самого слова (например, на английском языке)
    word = models.CharField(max_length=255, unique=True, verbose_name="Слово")

    # Поле для перевода слова (например, на русский язык)
    translation = models.CharField(max_length=255, blank=True, null=True, verbose_name="Перевод")

    # Поле для изображения, связанного со словом (опционально)
    image = models.OneToOneField(
        ImageModel,
        blank=True,
        null=True,
        verbose_name="Изображения",
        on_delete=models.SET_NULL
    )

    # Поле для даты создания записи
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    # Поле для даты последнего обновления записи
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return f"{self.word} - {self.translation}"

    class Meta:
        verbose_name = "Карточка слова"
        verbose_name_plural = "Карточки слов"