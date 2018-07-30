from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic.list import ListView

from cms.models import Book, Impression
from cms.forms import BookForm, ImpressionForm

import requests

# Create your views here.
def book_list(request):
    """書籍の一覧"""
    # return HttpResponse('書籍の一覧')
    books = Book.objects.all().order_by('id')
    return render(request, 'cms/book_list.html', {'books': books})

def book_edit(request, book_id=None):
    """書籍の編集"""
    # return HttpResponse('書籍の編集')
    if book_id:
        book = get_object_or_404(Book, pk=book_id)
    else:
        book = Book()

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save(commit=False)
            book.save()
            return redirect('cms:book_list')
    else:
        form = BookForm(instance=book)

    return render(request, 'cms/book_edit.html', dict(form=form, book_id=book_id))

def book_del(request, book_id):
    """書籍の削除"""
    # return HttpResponse('書籍の削除')
    book = get_object_or_404(Book, pk=book_id)
    book.delete()
    return redirect('cms:book_list')

def book_search(request):
    """"書籍の検索"""
    # return HttpResponse('書籍の検索')
    book = Book()

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save(commit=False)
            book.save()
            # print(type(book))
            # print(type(str(book)))
            search = str(book).split()
            # print(search)
            if len(search) > 1:
                isbn = search[1]
                isbn = isbn.replace("-", "")
                headers = {"content-type": "application/json"}
                res = requests.get('https://www.googleapis.com/books/v1/volumes?q=isbn:%s' % isbn, headers=headers)
                data = res.json()
                if data['totalItems'] > 0:
                    title = data['items'][0]['volumeInfo']['title']
                    publish_date = data['items'][0]['volumeInfo']['publishedDate']
                    isbn = data['items'][0]['volumeInfo']['industryIdentifiers'][1]['identifier']
                    authors = data['items'][0]['volumeInfo']['authors']
                    page =  data['items'][0]['volumeInfo']['pageCount']
                    form = BookForm(initial={'name': title, 'publisher': authors, 'page': page, 'publish_date': publish_date, 'isbn': isbn})
                    # return redirect('cms:book_search_result')
                    return render(request, 'cms/book_edit.html', {'form': form,})
            elif len(search) == 1:
                title = search[0]
                headers = {"content-type": "application/json"}
                res = requests.get('https://www.googleapis.com/books/v1/volumes?q=%s' % title, headers=headers)
                data = res.json()
                books = []
                if data['totalItems'] > 0:
                    for i in range(len(data['items'])):
                        try:
                            name = data['items'][i]['volumeInfo']['title']
                            author = data['items'][i]['volumeInfo']['authors']
                            pagecount = data['items'][i]['volumeInfo']['pageCount']
                            publish_date = data['items'][i]['volumeInfo']['publishedDate']
                            isbn = data['items'][i]['volumeInfo']['industryIdentifiers'][1]['identifier']
                            info = {'name': name, 'author': author, 'pageCount': pagecount, 'publish_date': publish_date, 'isbn': isbn}
                            books.append(info)
                        except:
                            continue
                    # booksの中の辞書配列の内容をclass Bookに入れて返したい
                    # books = BookForm(initial={'name': title, 'publisher': authors, 'page': page, 'publish_date': publish_date, 'isbn': isbn})

                    # return redirect('cms:book_search_result')
                    return render(request, 'cms/book_search_list.html', {'books': books,})

            else:
                form = BookForm(instance=book)
    else:
        form = BookForm(instance=book)

    return render(request, 'cms/book_search.html', dict(form=form))

class ImpressionList(ListView):
    """感想の一覧"""
    context_object_name = 'impressions'
    template_name = 'cms/impression_list.html'
    paginate_by = 2

    def get(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=kwargs['book_id'])
        impressions = book.impressions.all().order_by('id')
        self.object_list = impressions

        context = self.get_context_data(object_list=self.object_list, book=book)
        return self.render_to_response(context)

def impression_edit(request, book_id, impression_id=None):
    """感想の編集"""
    book = get_object_or_404(Book, pk=book_id)  # 親の書籍を読む
    if impression_id:   # impression_id が指定されている (修正時)
        impression = get_object_or_404(Impression, pk=impression_id)
    else:               # impression_id が指定されていない (追加時)
        impression = Impression()

    if request.method == 'POST':
        form = ImpressionForm(request.POST, instance=impression)  # POST された request データからフォームを作成
        if form.is_valid():    # フォームのバリデーション
            impression = form.save(commit=False)
            impression.book = book  # この感想の、親の書籍をセット
            impression.save()
            return redirect('cms:impression_list', book_id=book_id)
    else:    # GET の時
        form = ImpressionForm(instance=impression)  # impression インスタンスからフォームを作成

    return render(request, 'cms/impression_edit.html', dict(form=form, book_id=book_id, impression_id=impression_id))

def impression_del(request, book_id, impression_id):
    """感想の削除"""
    impression = get_object_or_404(Impression, pk=impression_id)
    impression.delete()
    return redirect('cms:impression_list', book_id=book_id)
