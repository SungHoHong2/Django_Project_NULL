from rest_framework import serializers
from member.models import MyUser

class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ('username', 'password')



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = '__all__'
