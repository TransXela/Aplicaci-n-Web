from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.models import TxdChofer
from app.serializables import TxdChoferS, ChoferesDenuncias
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

@api_view(['GET', 'POST'])
def lista_objetos(request):
    """
    Lista de todos los choferes, o crea uno nuevo
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
            serializador = TxdChoferS(objeto, many = true)
            return Response(serializador.data)
        else:
            content = {'Permiso denegado': 'El usuario no tiene permisos para visualizar datos'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)


    elif request.method == 'POST':
        if usuario.has_perm('app.add_txdchofer'):
            serializador = TxdChoferS(data = request.data)
            if serializador.is_valid():
                serializador.save()
                return Response(serializador.data, status=status.HTTP_201_CREATED)
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            content = {'Permiso denegado': 'El usuario no tiene permisos para ingresar datos'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET', 'PUT', 'DELETE'])
def detalle_objetos(request, pk):
    """
    Actuliza o elimina o chofer segun su id
    """
    try:
        objToken = Token.objects.get(key=request.query_params.get('tk'))
        usuario = User.objects.get(pk=objToken.user.id)
    except ObjectDoesNotExist:
        content = {'Datos incorrectos': 'El token enviado no coincide para ningun usuario'}
        return Response(content, status=status.HTTP_403_FORBIDDEN)

    try:
        objeto = TxdChofer.objects.get(pk=pk)
    except objeto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        if usuario.has_perm('app.view_txdchofer'):
            serializador = TxdChoferS(objeto)
            return Response(serializador.data)
        else:
            content = {'Permiso denegado': 'El usuario no tiene permisos para visualizar datos'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)


    elif request.method == 'PUT':
        if usuario.has_perm('app.change_txdchofer'):
            serializador = TxdChoferS(objeto, data=request.data)
            if serializador.is_valid():
                serializador.save()
                return Response(serializador.data)
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            content = {'Permiso denegado': 'El usuario no tiene permisos para editar datos'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)


    elif request.method == 'DELETE':
        if usuario.has_perm('app.delete_txdchofer'):
            objeto.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            content = {'Permiso denegado': 'El usuario no tiene permisos para eliminar datos'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
def lista_choferes_denuncias(request):
    """
    Lista de todos los choferes con sus denuncias
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
            serializador = ChoferesDenuncias(objeto)
            return Response(serializador.data)
        else:
            content = {'Permiso denegado': 'El usuario no tiene permisos para visualizar datos'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
def chofer_dpi(request, pk):
    """
    Obtiene un Chofer segun su dpi
    """
    try:
        objToken = Token.objects.get(key=request.query_params.get('tk'))
        usuario = User.objects.get(pk=objToken.user.id)
    except ObjectDoesNotExist:
        content = {'Datos incorrectos': 'El token enviado no coincide para ningun usuario'}
        return Response(content, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        if usuario.has_perm('app.view_txdchofer'):
            try:
                objeto = TxdChofer.objects.get(dpi=pk)
            except objeto.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            serializador = TxdChoferS(objeto)
            return Response(serializador.data)
        else:
            content = {'Permiso denegado': 'El usuario no tiene permisos para visualizar datos'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
