from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from market.models import Enterprise
from rest_framework import serializers


class EnterpriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enterprise
        fields = [
            'id', 'name', 'category'
        ]


class ProductListView(ListModelMixin, GenericAPIView):
    queryset = Enterprise.objects.all()
    serializer_class = EnterpriseSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
