from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, viewsets

from aelithrastay.permissions import IsAdminOrSelf
from .serializers import RegisterSerializer, UserSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdminOrSelf)

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all().order_by('id')
        return User.objects.filter(id=self.request.user.id)
