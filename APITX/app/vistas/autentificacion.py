from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from app.models import TxdDuenio, TxdPmt, TxcCultura
from app.serializables import UserSerializer, TxdPmtS, TxdDuenioS, TxcCulturaS, GroupSerializer
from django.db import connection

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
            return Response("susuario y contasenia incorrecta", tatus=status.HTTP_404_NOT_FOUND)

def autenticacion(tk):
    try:
        token = Token.objects.get(key=tk)
        usuario = User.objects.get(pk=token.user.id)
        return usuario
    except objeto.DoesNotExist:
        return Response("datos incorrectos", status=status.HTTP_403_NOT_FOUND)
