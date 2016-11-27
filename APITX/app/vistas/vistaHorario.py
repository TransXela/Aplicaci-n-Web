from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from datetime import datetime
from app.models import TxdHorario
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from app.serializables import TxdHorarioS

@api_view(['GET', 'POST'])
def lista_objetos(request):
    """
    Lista de todos los Horarios, o crea uno nuevo.
    """
    try:
        objToken = Token.objects.get(key=request.query_params.get('tk'))
        usuario = User.objects.get(pk=objToken.user.id)
    except ObjectDoesNotExist:
        content = {'Datos incorrectos': 'El token enviado no coincide para ningun usuario'}
        return Response(content, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        if usuario.has_perm('app.view_txdhorario'):
            objeto = TxdHorario.objects.all()
            serializador = TxdHorarioS(objeto, many=True)
            return Response(serializador.data)
        else:
            content = {'Permiso denegado': 'El usuario no tiene permisos para visualizar los datos'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)


    elif request.method == 'POST':
        if usuario.has_perm('app.add_txdhorario'):
            serializador = TxdHorarioS(data=request.data)
            if serializador.is_valid():
                inicio = datetime.strptime(str(request.data.get('horainicio')),'%H:%M')
                final = datetime.strptime(str(request.data.get('horafin')),'%H:%M')
                if (final > inicio):
                    serializador.save()
                    return Response(serializador.data, status=status.HTTP_201_CREATED)
                else:
                    respuesta ={"crear": {"estado": "Hora inicio debe ser menor o diferente a la hora final"}}
                    return Response(respuesta, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            content = {'Permiso denegado': 'El usuario no tiene permisos para ingresar datos'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET', 'PUT', 'DELETE'])
def detalle_objetos(request, pk):
    """
    Actualiza, elimina un objeto segun su id
    """
    try:
        objToken = Token.objects.get(key=request.query_params.get('tk'))
        usuario = User.objects.get(pk=objToken.user.id)
    except ObjectDoesNotExist:
        content = {'Datos incorrectos': 'El token enviado no coincide para ningun usuario'}
        return Response(content, status=status.HTTP_403_FORBIDDEN)

    try:
        objeto = TxdHorario.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        if usuario.has_perm('app.view_txdhorario'):
            serializador = TxdHorarioS(objeto)
            return Response(serializador.data)
        else:
            content = {'Permiso denegado': 'El usuario no tiene permisos para visualizar los datos'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)

    elif request.method == 'PUT':
        if usuario.has_perm('app.change_txdhorario'):
            serializador = TxdHorarioS(objeto, data=request.data)
            if serializador.is_valid():
                inicio = datetime.strptime(str(request.data.get('horainicio')),'%H:%M')
                final = datetime.strptime(str(request.data.get('horafin')),'%H:%M')
                if final>inicio:
                    serializador.save()
                    respuesta ={"modificar": {"estado": "Horario modificado exitosamente"}}
                    return Response(respuesta, status=status.HTTP_201_CREATED)
                else:
                    respuesta ={"modificar": {"estado": "Hora inicio debe ser menor o diferente a la hora final"}}
                    return Response(respuesta, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            content = {'Permiso denegado': 'El usuario no tiene permisos para editar datos'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)

    elif request.method == 'DELETE':
        if usuario.has_perm('app.delete_txdhorario'):
            try:
                objeto.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except IntegrityError:
                content = {'estado': 'No se puede eliminar tiene dependencias'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            content = {'Permiso denegado': 'El usuario no tiene permisos para eliminar datos'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)



@api_view(['GET'])
def horarios_duenio(request, pk):
    """
    obtiene los horarios de un duenio
    """
    try:
        objToken = Token.objects.get(key=request.query_params.get('tk'))
        usuario = User.objects.get(pk=objToken.user.id)
    except ObjectDoesNotExist:
        content = {'Datos incorrectos': 'El token enviado no coincide para ningun usuario'}
        return Response(content, status=status.HTTP_403_FORBIDDEN)


    if request.method == 'GET':
        if usuario.has_perm('app.view_txdhorario'):
            try:
                objeto = TxdHorario.objects.filter(duenio=pk)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            serializador = TxdHorarioS(objeto, many=True)
            return Response(serializador.data)
        else:
            content = {'Permiso denegado': 'El usuario no tiene permisos para visualizar los datos'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
