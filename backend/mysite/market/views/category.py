from market.models import Category

from rest_framework import serializers
from rest_framework import viewsets
from rest_framework import permissions


class CategorySeryalizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class CategoryViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows users to read and modify categories.
    """

    queryset = Category.objects.all().order_by('-id')
    serializer_class = CategorySeryalizer
    permissions_classes = [permissions.AllowAny]
    http_method_names = ['get', 'post']
