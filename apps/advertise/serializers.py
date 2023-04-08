from rest_framework import serializers
from .models import *

class AdvertiseImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['id', 'image']


class AdvertiseSerializer(serializers.ModelSerializer):
    owner_id = serializers.ReadOnlyField(source = 'owner.id')
    owner_name = serializers.ReadOnlyField(source='owner.username') #Get username instead of id
    images = AdvertiseImageSerializer(many = True, read_only=True)
    uploaded_images = serializers.ListField(required=False,
    child = serializers.ImageField( max_length=1000000, allow_empty_file = True,
    use_url = False, allow_null= True, )
    ,write_only= True ) #List field to enable multiple images

    class Meta:
        model = Advertise
        fields = ['id', 'owner_id', 'owner_name',  'category', 'description',
         'price', 'expiration_date', 'created_at', 'images', 'uploaded_images', 'is_active']

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        advertise = Advertise.objects.create(**validated_data)
        for image in uploaded_images:
            new_advertise_image = Images.objects.create(advertise = advertise, image = image)   
        return advertise