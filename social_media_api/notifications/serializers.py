from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class NotificationSerializer(serializers.ModelSerializer):
    actor = ActorSerializer(read_only=True)
    target_type = serializers.SerializerMethodField()
    target_id = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = ['id', 'actor', 'verb', 'target_type', 'target_id', 'timestamp', 'read']
        read_only_fields = ['id', 'timestamp']
    
    def get_target_type(self, obj):
        if obj.target:
            return obj.target._meta.model_name
        return None
    
    def get_target_id(self, obj):
        if obj.target:
            return obj.target.id
        return None
