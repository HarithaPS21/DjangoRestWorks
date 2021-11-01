from django.shortcuts import render
from rest_framework.views import APIView
from .models import Todo
from .serializers import TodoSerializer, UserCreationSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins, generics
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

# api/v1/todos  (get)   -  list all todos
# api/v1/todos  (post)  -  create a new todo

# api/v1/todos/{id}  (get)  -  detail of a specific todo
# api/v1/todos/{id}  (put)  -  update a specific todo
# api/v1/todos/{id}  (delete) - delete a specific todo


class TodoList(APIView):
    model = Todo
    serializer_class = TodoSerializer

    def get(self,request):
        todos = self.model.objects.all()
        serializer = self.serializer_class(todos,many=True)  # many todos
        return Response(serializer.data, status=status.HTTP_200_OK)  # status = success

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoDetails(APIView):
    model = Todo
    serializer_class = TodoSerializer

    def get_object(self, id):
        return self.model.objects.get(id=id)

    def get(self,request,*args,**kwargs):
        id = kwargs['id']
        todo = self.get_object(id)
        serializer = self.serializer_class(todo)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self,request,*args,**kwargs):
        id = kwargs['id']
        todo = self.get_object(id)
        serializer = self.serializer_class(todo,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,*args,**kwargs):
        todo = self.get_object(kwargs["id"])
        todo.delete()
        return Response(status=status.HTTP_200_OK)
# mixins - ListModelMixin,CreateModelMixin,UpdateModelMixin,DestroyModelMixin


class TodoListMixin(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    model = Todo
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def perform_create(self, serializer):
        user = self.request.user
        print(user)
        serializer.save(user=user)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)


class TodoDetailMixin(generics.GenericAPIView,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin):
    model = Todo
    serializer_class = TodoSerializer
    queryset = model.objects.all()
    lookup_field = 'id'
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)

    def perform_update(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)


class UserCreationView(generics.GenericAPIView, mixins.CreateModelMixin):
    model = User
    serializer_class = UserCreationSerializer

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)


class LoginView(APIView):
    model = User
    serializer_class = LoginSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request,user)
                return Response({"msg":"login success"}, status=status.HTTP_200_OK)
            else:
                return Response({"msg":"login failed"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors)


