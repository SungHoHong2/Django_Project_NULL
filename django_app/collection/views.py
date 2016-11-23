from django.shortcuts import render
from collection.serializer import ImageSerializer

# Create your views here.
from rest_framework import viewsets


class ImageActionView(viewsets.ModelViewSet):
    # Image upload without parentId
    serializer_class = ImageSerializer

