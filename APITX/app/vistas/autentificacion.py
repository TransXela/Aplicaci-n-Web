from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from app.models import TxdDuenio, TxdPmt, TxcCultura
from app.serializables import UserSerializer, TxdPmtS, TxdDuenioS, TxcCulturaS

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
            if TxdPmt.objects.filter(usuario=objUsuario.pk).exists():
                datos['usuario'] = TxdPmtS(TxdPmt.objects.get(usuario=objUsuario.pk)).data
            elif TxdDuenio.objects.filter(usuario=objUsuario.pk).exists():
                datos['usuario'] = TxdDuenioS(TxdDuenio.objects.get(usuario=objUsuario.pk)).data
            elif TxcCultura.objects.filter(usuario=objUsuario.pk).exists():
                datos['usuario'] = TxcCulturaS(TxcCultura.objects.get(usuario=objUsuario.pk)).data
            token, created = Token.objects.get_or_create(user=objUsuario)
            datos['token'] = token.key
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
