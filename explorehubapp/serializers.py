from .models import *
from rest_framework import serializers


class exploreSerializers(serializers.ModelSerializer):
    explore_img = serializers.ImageField(required=False)

    class Meta:
        model = Destinations
        fields = '__all__'
