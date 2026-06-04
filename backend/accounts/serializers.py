from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import AdminLog

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'phone',
            'avatar',
            'bio',
            'is_suspended',
        )
        read_only_fields = ('id',)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'role',
            'phone',
        )
        read_only_fields = ('id',)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class EmailOrUsernameTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get(self.username_field)
        if username and '@' in username:
            users = User.objects.filter(email__iexact=username)
            if users.exists():
                user = users.filter(is_staff=True).first() or users.filter(is_superuser=True).first() or users.filter(role__iexact='admin').first() or users.first()
                attrs[self.username_field] = user.get_username()

        data = super().validate(attrs)

        if self.user.is_suspended:
            raise serializers.ValidationError('This account has been suspended.')

        return data


class AdminUserSerializer(serializers.ModelSerializer):
    """Detailed user info for admin panel"""
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'phone',
            'avatar',
            'bio',
            'is_suspended',
            'is_staff',
            'date_joined',
        )
        read_only_fields = ('id', 'date_joined')


class AdminLogSerializer(serializers.ModelSerializer):
    admin_username = serializers.CharField(source='admin.username', read_only=True)
    
    class Meta:
        model = AdminLog
        fields = (
            'id',
            'admin',
            'admin_username',
            'action_type',
            'object_type',
            'object_id',
            'details',
            'created_at',
        )
        read_only_fields = ('id', 'admin', 'created_at')


class UserSuspensionSerializer(serializers.Serializer):
    """Handle user suspension/activation"""
    is_suspended = serializers.BooleanField()

    def update(self, instance, validated_data):
        instance.is_suspended = validated_data.get('is_suspended', instance.is_suspended)
        instance.save()
        return instance


class UserRoleChangeSerializer(serializers.Serializer):
    """Handle user role changes"""
    role = serializers.ChoiceField(choices=['guest', 'host', 'admin'])

    def update(self, instance, validated_data):
        instance.role = validated_data.get('role', instance.role)
        instance.save()
        return instance
