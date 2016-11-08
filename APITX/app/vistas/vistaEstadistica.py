from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.models import TxdDenuncia, TxdBus, TxdRuta, TxdChofer, TxdDuenio
from app.serializables import TxdDenunciaS, BusRutaS, ChoferDenunciaS, BusDuenioS
from app.vistas import autentificacion
from app import permisos
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

@api_view(['GET'])
def lista_objetos(request):

    """
    Lista todas las denuncias
    """
    try:
        objToken = Token.objects.get(key=request.query_params.get('tk'))
        usuario = User.objects.get(pk=objToken.user.id)
    except ObjectDoesNotExist:
        content = {'Datos incorrectos': 'El token enviado no coincide para ningun usuario'}
        return Response(content, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        objeto = TxdDenuncia.objects.all()
        serializador = TxdDenunciaS(objeto, many=True)
        return Response(serializador.data)

@api_view(['GET'])
def lista_objetos_rutaBus(request):

    """
    Lista todos las rutas y buses
    """
    try:
        objToken = Token.objects.get(key=request.query_params.get('tk'))
        usuario = User.objects.get(pk=objToken.user.id)
    except ObjectDoesNotExist:
        content = {'Datos incorrectos': 'El token enviado no coincide para ningun usuario'}
        return Response(content, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        objeto = TxdRuta.objects.all()
        serializador = BusRutaS(objeto, many=True)
        return Response(serializador.data)

@api_view(['GET'])
def lista_objetos_pilotoDenuncia(request):

    """
    Lista todos las rutas y buses
    """
    try:
        objToken = Token.objects.get(key=request.query_params.get('tk'))
        usuario = User.objects.get(pk=objToken.user.id)
    except ObjectDoesNotExist:
        content = {'Datos incorrectos': 'El token enviado no coincide para ningun usuario'}
        return Response(content, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        objeto = TxdChofer.objects.all()
        serializador = ChoferDenunciaS(objeto, many=True)
        return Response(serializador.data)

@api_view(['GET'])
def lista_objetos_duenioBuses(request):

    """
    Lista todos los buses de un duenio
    """
    try:
        objToken = Token.objects.get(key=request.query_params.get('tk'))
        usuario = User.objects.get(pk=objToken.user.id)
    except ObjectDoesNotExist:
        content = {'Datos incorrectos': 'El token enviado no coincide para ningun usuario'}
        return Response(content, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        objeto = TxdDuenio.objects.all()
        serializador = BusDuenioS(objeto, many=True)
        return Response(serializador.data)
