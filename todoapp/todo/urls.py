from django.urls import path
from todo import views


urlpatterns=[
    # path('todos', views.TodoList.as_view()),
    # path('todos/<int:id>', views.TodoDetails.as_view()),

    path('todos', views.TodoListMixin.as_view()),
    path('todos/<int:id>', views.TodoDetailMixin.as_view()),
    path('todos/accounts/signup', views.UserCreationView.as_view()),
    path('todos/accounts/signin', views.LoginView.as_view())
]

