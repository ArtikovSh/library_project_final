from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Book


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ('id', 'title', 'subtitle', 'content', 'author', 'isbn', 'price')

    def validate(self, data):
        title = data.get("title", None)
        author = data.get("author", None)

        # Check title if it contains only alphabetical chars
        if not title.isalpha():
            raise ValidationError({
                "status": False,
                "message": "Kitob sarlavhasi harflardan tashkil topgan bo'lishi kerak"
            })

        # Check title and author if they exist in database
        if Book.objects.filter(title=title, author=author).exists():
            raise ValidationError({
                "status": False,
                "message": "Ushbu kitob ma'lumotlar bazasida mavjud!"
            })
        return data

    def validate_price(self, price):
        if price < 0 or price > 999999:
            raise ValidationError({
                "status": False,
                "message": "Narx noto'g'ri kiritildi!"
            })
        return price