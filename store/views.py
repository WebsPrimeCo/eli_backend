from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import models
from . import serializers


@api_view(['GET'])
def category_view(request):
    category_queryset = models.Category.objects.all()
    serializer = serializers.CategorySerializer(data= category_queryset)
    return Response(serializer)

