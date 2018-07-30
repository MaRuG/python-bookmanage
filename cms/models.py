from django.db import models

# Create your models here.
class Book(models.Model):
    """書籍"""
    name = models.CharField('書籍名', max_length=255)
    publisher = models.CharField('著者', max_length=255, blank=True)
    page = models.IntegerField('ページ数', blank=True, default=0)
    publish_date = models.CharField('出版日', max_length=255, blank=True)
    isbn = models.CharField('ISBN', max_length=13, blank=True)

    def __str__(self):
        template = '{0.name} {0.isbn}'
        # return self.name, self.isbn
        return template.format(self)


class Impression(models.Model):
    """感想"""
    book = models.ForeignKey(Book, verbose_name='書籍', related_name='impressions', on_delete=models.CASCADE)
    comment = models.TextField('コメント', blank=True)

    def __str__(self):
        return self.comment
