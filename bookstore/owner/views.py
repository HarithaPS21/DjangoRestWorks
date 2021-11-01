from django.shortcuts import render
from rest_framework.views import APIView
from .models import Book
from .serializers import BookSerializer
from rest_framework.response import Response
from rest_framework import status

from rest_framework import mixins,generics


class BookList(APIView):
    model = Book
    serializer_class = BookSerializer

    def get(self,request):
        books = self.model.objects.all()
        serializer = self.serializer_class(books,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class BookDetails(APIView):
    model = Book
    serializer_class = BookSerializer

    def get_object(self,id):
        return self.model.objects.get(id=id)

    def get(self,request,*args,**kwargs):
        book = self.get_object(kwargs['id'])
        serializer = self.serializer_class(book)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self,request,*args,**kwargs):
        book =self.get_object(kwargs['id'])
        serializer = self.serializer_class(book,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,*args,**kwargs):
        book = self.get_object(kwargs['id'])
        book.delete()
        return Response(status=status.HTTP_200_OK)

# same views implemented using builtin views in mixins module
# rest_framework -> mixins module -> ListModelMixin,CreateModelMixin,UpdateModelMixin,DestroyModelMixin


class BookListMixin(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    model = Book
    serializer_class = BookSerializer
    queryset = model.objects.all()

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)


class BookDetailMixin(generics.GenericAPIView,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin):
    model = Book
    serializer_class = BookSerializer
    queryset = model.objects.all()
    lookup_field = 'id'

    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)

    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)





