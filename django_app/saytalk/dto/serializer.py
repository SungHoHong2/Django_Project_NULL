from rest_framework import serializers
from saytalk.models import SayTalk

class SayTalkPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = SayTalk
        fields = ('id', 'title', 'content', 'created_by')

