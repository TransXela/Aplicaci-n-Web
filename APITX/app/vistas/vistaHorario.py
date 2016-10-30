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
from app import permisos
from app.vistas import autentificacion

@api_view(['GET', 'POST'])
def lista_objetos(request, tk):
    """
    Lista de todos los Horarios, o crea uno nuevo.
    """
    usuario = autentificacion.autenticacion(tk)
    if usuario.has_perms(permisos.duenios):
        if request.method == 'GET':
            objeto = TxdHorario.objects.all()
            serializador = TxdHorarioS(objeto, many=True)
            return Response(serializador.data)

        elif request.method == 'POST':
            serializador = TxdHorarioS(data=request.data)
            if serializador.is_valid():
                inicio = datetime.strptime(str(request.data.get('horainicio')),'%H:%M')
                final = datetime.strptime(str(request.data.get('horafin')),'%H:%M')
                if (final > inicio):
                    serializador.save()
                    return Response(serializador.data, status=status.HTTP_201_CREATED)
                else:
                    respuesta ={"crear": {"estado": "Hora inicio debe ser menor/diferente a hora fin"}}
                    return Response(respuesta, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("No tiene los permisos necesarios", status=status.HTTP_403_NOT_FOUND)

@api_view(['GET', 'PUT', 'DELETE'])
def detalle_objetos(request, pk, tk):
    """
    Actualiza, elimina un objeto segun su id
    """

    usuario = autentificacion.autenticacion(tk)
    if usuario.has_perms(permisos.duenios):
        try:
            objeto = TxdHorario.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializador = TxdHorarioS(objeto)
            return Response(serializador.data)

        elif request.method == 'PUT':
            serializador = TxdHorarioS(objeto, data=request.data)
            if serializador.is_valid():
                inicio = datetime.strptime(str(request.data.get('horainicio')),'%H:%M')
                final = datetime.strptime(str(request.data.get('horafin')),'%H:%M')
                if final>inicio:
                    serializador.save()
                    respuesta ={"modificar": {"estado": "Horario modificado exitosamente"}}
                    return Response(respuesta, status=status.HTTP_201_CREATED)
                else:
                    respuesta ={"modificar": {"estado": "Hora inicio debe ser menor/diferente a hora fin"}}
                    return Response(respuesta, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            try:
                objeto.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except IntegrityError:
                content = {'estado': 'No se puede eliminar tiene dependencias'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("No tiene los permisos necesarios", status=status.HTTP_403_NOT_FOUND)

@api_view(['GET'])
def horarios_duenio(request, pk, tk):
    """
    obtiene los horarios de un duenio
    """
    usuario = autentificacion.autenticacion(tk)
    if usuario.has_perms(permisos.duenios):
        try:
            objeto = TxdHorario.objects.filter(duenio=pk)
        except objeto.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializador = TxdHorarioS(objeto, many=True)
            return Response(serializador.data)
    else:
        return Response("No tiene los permisos necesarios", status=status.HTTP_403_NOT_FOUND)
