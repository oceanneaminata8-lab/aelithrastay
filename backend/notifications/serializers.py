from rest_framework import serializers

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    user_name = serializers.StringRelatedField(source='user', read_only=True)

    class Meta:
        model = Notification
        fields = ('id', 'user', 'user_name', 'title', 'message', 'is_read', 'created_at')
        read_only_fields = ('id', 'created_at')
