from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model

from .serializers import RegisterSerializerCustom

# Create your views here.
class UserCreate(CreateAPIView):
    """
    Creates the user.
    """

    model = get_user_model()
    serializer_class = RegisterSerializerCustom