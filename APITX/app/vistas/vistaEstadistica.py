from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.models import TxdDenuncia, TxdBus, TxdRuta, TxdChofer, TxdDuenio
from app.serializables import TxdDenunciaS, BusRutaS, ChoferDenunciaS, BusDuenioS
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
        if usuario.has_perm('app.view_txddenuncia'):
            objeto = TxdDenuncia.objects.all()
            serializador = TxdDenunciaS(objeto, many=True)
            return Response(serializador.data)
        else:
            content = {'Permiso denegado': 'El usuario no tiene permisos'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)

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
        if usuario.has_perm('app.view_txdruta'):
            objeto = TxdRuta.objects.all()
            serializador = BusRutaS(objeto, many=True)
            return Response(serializador.data)
        else:
            content = {'Permiso denegado': 'El usuario no tiene permisos'}

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
        if usuario.has_perm('app.view_txdchofer'):
            objeto = TxdChofer.objects.all()
            serializador = ChoferDenunciaS(objeto, many=True)
            return Response(serializador.data)
        else:
            content = {'Permiso denegado':'El usuario no tiene permisos'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)

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
        if usuario.has_perm('app.view_txdduenio'):
            objeto = TxdDuenio.objects.all()
            serializador = BusDuenioS(objeto, many=True)
            return Response(serializador.data)
        else:
            content = {'Permiso denado': 'El usuario no tiene permisos'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def lista_objetos_duenioBusesId(request, pk):

    """
    Lista todos los buses de un duenio por id
    """
    try:
        objeto = TxdDuenio.objects.get(pk=pk)
    except objeto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializador = BusDuenioS(objeto)
        return Response(serializador.data)

@api_view(['GET'])
def lista_objetos_duenioChofId(request, pk):

    """
    Lista todos los pilotos de un duenio por id
    """
    try:
        objeto = TxdDuenio.objects.get(pk=pk)
    except objeto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializador = PilotoDuenioS(objeto)
        return Response(serializador.data)

@api_view(['GET'])
def lista_objetos_busChofId(request, pk):

    """
    Lista todos los buses de un duenio por id
    """
    try:
        objeto = TxdBus.objects.filter(duenio=pk)
    except objeto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializador = TxdBusS(objeto, many=True)
        return Response(serializador.data)

@api_view(['GET'])
def lista_objetos_tipoDenDenuncia(request):

    """
    Lista todas las denuncias
    """
    if request.method == 'GET':
        if usuario.has_perm('app.views_txdTipodenuncia'):
            objeto = TxdTipodenuncia.objects.all()
            serializador = TipoDenDenunciaS(objeto, many=True)
            return Response(serializador.data)
        else:
            content = {'Permiso denagado': 'El usuario no tiene permisos'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
