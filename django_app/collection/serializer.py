from rest_framework import serializers
from collection.models import Image

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id','img_file', 'img_order')

