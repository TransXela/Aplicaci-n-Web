from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group,PermissionsMixin
from app.serializables import GroupSerializer,PermisionS
from app import permisos
from app.vistas import autentificacion

@api_view(['GET', 'POST'])
def lista_objetos(request, pk):
    """
    Lista de todas las Buses, o crear una nueva
    """
    usuario = autentificacion.autenticacion(tk)
    if usuario.has_perms(permisos.lista_duenios):
        if request.method == 'GET':
            objeto = PermissionsMixin().groups
            print objeto
            serializador = PermisionS(objeto)
            return Response(serializador.data)

        elif request.method == 'POST':
            serializador = GroupSerializer(data=request.data)
            if serializador.is_valid():
                serializador.save()
                return Response(serializador.data, status=status.HTTP_201_CREATED)
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("No tiene los permisos necesarios", status=status.HTTP_403_NOT_FOUND)

@api_view(['GET', 'PUT','DELETE'])
def detalle_objetos(request, pk):
    """
    Actualiza, elimina un objeto segun su id
    """
    usuario = autentificacion.autenticacion(tk)
    if usuario.has_perms(permisos.lista_duenios):
        try:
            objeto = Group.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


        if request.method == 'GET':
            serializador = GroupSerializer(objeto)
            return Response(serializador.data)

        elif request.method == 'PUT':
            serializador = GroupSerializer(objeto, data=request.data)
            if serializador.is_valid():
                serializador.save()
                return Response(serializador.data)
            return Response(serializador.errors,status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            objeto.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response("No tiene los permisos necesarios", status=status.HTTP_403_NOT_FOUND)

@api_view(['GET',])
def Grupo_Usuario(request, pk):
    """
    Lista de todas las Buses, o crear una nueva
    """
    usuario = autentificacion.autenticacion(tk)
    if usuario.has_perms(permisos.lista_duenios):
        if request.method == 'GET':
            objeto = Group.objects.all()

            serializador = GroupSerializer(objeto, many=True)
            return Response(serializador.data)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("No tiene los permisos necesarios", status=status.HTTP_403_NOT_FOUND)
