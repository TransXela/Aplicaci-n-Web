from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import IntegrityError
from app.models import TxdRuta
from app.serializables import TxdRutaS


@api_view(['GET', 'POST'])
def lista_objetos(request):
    """
    Lista de todos los Rutas, o crea uno nuevo.
    """
    if request.user.has_perms(permisos.lista_duenios):
        if request.method == 'GET':
            objeto = TxdRuta.objects.all()
            serializador = TxdRutaS(objeto, many=True)
            return Response(serializador.data)

        elif request.method == 'POST':
            serializador = TxdRutaS(data=request.data)
            if serializador.is_valid():
                serializador.save()
                return Response(serializador.data, status=status.HTTP_201_CREATED)
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_403_NOT_FOUND)


@api_view(['GET', 'PUT', 'DELETE'])
def detalle_objetos(request, pk):
    """
    Actuliza, elimina un objeto segun su id
    """
    if request.user.has_perms(permisos.lista_duenios):
        try:
            objeto = TxdRuta.objects.get(pk=pk)
        except objeto.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializador = TxdRutaS(objeto)
            return Response(serializador.data)

        elif request.method == 'PUT':
            serializador = TxdRutaS(objeto, data=request.data)
            if serializador.is_valid():
                serializador.save()
                return Response(serializador.data)
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            try:
                objeto.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except IntegrityError:
                content = {'estado': 'No se puede eliminar tiene dependencias'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_403_NOT_FOUND)
