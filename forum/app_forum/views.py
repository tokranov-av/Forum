from rest_framework.generics import CreateAPIView
from .serialisers import RegistrationSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationViewSet(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
