from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from app.models import TxdDenuncia
from app.serializables import TxdDenunciaS
from app import permisos
from app.vistas import autentificacion

@api_view(['GET', 'POST'])
def lista_objetos(request, tk):
    """
    Lista de todas las Buses, o crear una nueva
    """
    usuario = autentificacion.autenticacion(tk)
    if usuario.has_perms(permisos.lista_duenios):
        if request.method == 'GET':
            objeto = TxdDenuncia.objects.all()
            serializador = TxdDenunciaS(objeto, many=True)
            return Response(serializador.data)

        elif request.method == 'POST':
            serializador = TxdDenunciaS(data=request.data)
            if serializador.is_valid():
                serializador.save()
                return Response(serializador.data, status=status.HTTP_201_CREATED)
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("No tiene los permisos necesarios", status=status.HTTP_403_NOT_FOUND)

@api_view(['GET', 'PUT','DELETE'])
def detalle_objetos(request, pk, tk):
    """
    Actualiza, elimina un objeto segun su id
    """
    usuario = autentificacion.autenticacion(tk)
    if usuario.has_perms(permisos.lista_duenios):
        try:
            objeto = TxdDenuncia.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializador = TxdDenunciaS(objeto)
            return Response(serializador.data)

        elif request.method == 'PUT':
            serializador = TxdDenunciaS(objeto, data=request.data)
            if serializador.is_valid():
                serializador.save()
                return Response(serializador.data)
            return Response(serializador.errors,status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            objeto.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response("No tiene los permisos necesarios", status=status.HTTP_403_NOT_FOUND)

@api_view(['GET'])
def buses_Activos(request, tk):
    """
    retorna los busese que estan activos
    """
    usuario = autentificacion.autenticacion(tk)
    if usuario.has_perms(permisos.lista_duenios):
        try:
            objetos = TxdDenuncia.objects.filter(estado=1)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializador = TxdDenunciaS(objetos, many=True)
            return Response(serializador.data)
    else:
        return Response("No tiene los permisos necesarios", status=status.HTTP_403_NOT_FOUND)
