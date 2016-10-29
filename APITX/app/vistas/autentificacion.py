from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from app.serializables import UserSerializer
from app import permisos
from rest_framework.response import Response
#from rest_framework.decorators import api_view, authentication_classes, permission_classes


from rest_framework.authtoken.models import Token

"""

@api_view(['GET'])
#@authentication_classes((SessionAuthentication, BasicAuthentication,))
#@permission_classes((IsAuthenticated,))
def example_view(request, user, pass, format=None):
    content = {
        'user': unicode(user),  # `django.contrib.auth.User` instance.
        'auth': unicode(request.auth),  # None
    }
    return Response(content)
"""

@api_view(['POST'])
def token(request, format=None):
    """
    metodo para obtener un token de autentificacion y datos de usuario
    """
    if request.method == 'POST':
        try:
            objUsuario = User.objects.get(username = request.data.get('user'))
        except ObjectDoesNotExist:
            return Response("susuario y contasenia incorrecta", tatus=status.HTTP_404_NOT_FOUND)

        if objUsuario.check_password(request.data.get('pass')):
            datos = {}
            serUsuario = UserSerializer(objUsuario).data
            token, created = Token.objects.get_or_create(user=objUsuario)
            datos['usuario'] = serUsuario
            datos['token'] = token.key
            return Response(datos)
        else:
            return Response("susuario y contasenia incorrecta", tatus=status.HTTP_404_NOT_FOUND)
