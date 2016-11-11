from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token
from app.models import TxdDuenio, TxdPmt, TxcCultura
from app.serializables import UserSerializer, TxdPmtS, TxdDuenioS, TxcCulturaS, GroupSerializer
from django.db import connection


@api_view(['GET'])
#@authentication_classes((SessionAuthentication, BasicAuthentication,))
#@permission_classes((IsAuthenticated,))
def example_view(request, format=None):
    content = {
        'user': unicode(request.user),  # `django.contrib.auth.User` instance.
        'auth': unicode(request.auth),  # None
    }
    return Response(content)

@api_view(['POST'])
def token(request, format=None):
    """
    metodo para obtener un token de autentificacion y datos de usuario
    """
    if request.method == 'POST':
        try:
            objUsuario = User.objects.get(username = request.data.get('user'))
        except ObjectDoesNotExist:
            return Response("susuario y contasenia incorrecta", status=status.HTTP_404_NOT_FOUND)

        if objUsuario.check_password(request.data.get('pass')):

            datos = {}
            if TxdPmt.objects.filter(usuario=objUsuario.pk).exists():
                datos['PMT'] = TxdPmtS(TxdPmt.objects.get(usuario=objUsuario.pk)).data
            elif TxdDuenio.objects.filter(usuario=objUsuario.pk).exists():
                datos['Duenio'] = TxdDuenioS(TxdDuenio.objects.get(usuario=objUsuario.pk)).data
            elif TxcCultura.objects.filter(usuario=objUsuario.pk).exists():
                datos['Cultura'] = TxcCulturaS(TxcCultura.objects.get(usuario=objUsuario.pk)).data

            datos['Usuario'] = UserSerializer(objUsuario).data
            cursor = connection.cursor()
            cursor.execute("SELECT *FROM auth_user_groups WHERE user_id = %s", [objUsuario.pk])
            usuariogrupo = cursor.fetchall()
            datos['Grupo'] =  GroupSerializer(Group.objects.get(pk=usuariogrupo[0][2])).data
            token, created = Token.objects.get_or_create(user=objUsuario)
            datos['Token'] = token.key
            return Response(datos)
        else:
            return Response("susuario y contasenia incorrecta", status=status.HTTP_404_NOT_FOUND)
