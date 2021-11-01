from django.urls import path
from owner import views

urlpatterns = [
    # path('books', views.BookList.as_view()),
    # path('books/<int:id>', views.BookDetails.as_view()),
    path('books', views.BookListMixin.as_view()),
    path('books/<int:id>', views.BookDetailMixin.as_view())
]