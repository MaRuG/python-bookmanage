from django.forms import ModelForm
from cms.models import Book, Impression


class BookForm(ModelForm):
    """書籍のフォーム"""
    class Meta:
        model = Book
        fields = ('name', 'publisher', 'page', 'publish_date', 'isbn', )

class BookSearchForm(ModelForm):
    """書籍の検索フォーム"""
    class Meta:
        model = Book
        fields = ('name', 'publisher', 'page', 'publish_date', 'isbn', )

class ImpressionForm(ModelForm):
    class Meta:
        model = Impression
        fields = ('comment', )

