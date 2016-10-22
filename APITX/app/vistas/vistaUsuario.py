from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth.models import User
from app.serializables import UserSerializer
from app.models import TxdDuenio
from app.serializables import TxdDuenioS
from django.contrib.auth.hashers import PBKDF2PasswordHasher

@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication,))
@permission_classes((IsAuthenticated,))
def autenticar(request, format=None):

    if request.method == 'GET':
        try:
            objetoUsuario = User.objects.get(username=request.user)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        duenio = TxdDuenio.objects.get(usuario=objetoUsuario.id)
        serializador = TxdDuenioS(duenio)
        return Response(serializador.data)

        """
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(content)
        """


@api_view(['POST'])
def crear_usuario(request):
    """
    este metodo crea un nuevo usuario y retorna los datos creados
    """
    if request.method == 'POST':
        serializador = UserSerializer(data = request.data)
        if serializador.is_valid():
            user = User.objects.create_user(username=request.data.get('username'),
                                            email=request.data.get('email'),
                                            password=request.data.get('password'))
            user.save()
            return Response(UserSerializer(User.objects.get(username=user)).data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)
