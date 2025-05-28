from rest_framework import serializers
from .models import APIDocument, APIMessage, APIConversation


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIDocument
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIMessage
        fields = '__all__'


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIConversation
        fields = '__all__'
