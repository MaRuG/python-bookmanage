from django.urls import path
from cms import views

app_name = 'cms'
urlpatterns = [
    path('book/', views.book_list, name='book_list'),
    path('book/add/', views.book_edit, name='book_add'),
    path('book/search/', views.book_search, name='book_search'),
    path('book/mod/<int:book_id>/', views.book_edit, name='book_mod'),
    path('book/del/<int:book_id>/', views.book_del, name='book_del'),
    path('impression/<int:book_id>/', views.ImpressionList.as_view(), name='impression_list'),
    path('impression/add/<int:book_id>/', views.impression_edit, name='impression_add'),
    path('impression/mod/<int:book_id>/<int:impression_id>/', views.impression_edit, name='impression_mod'),
    path('impression/del/<int:book_id>/<int:impression_id>/', views.impression_del, name='impression_del'),
]
