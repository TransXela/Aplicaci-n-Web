from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from app.models import TxdTipodenuncia
from app.serializables import TxdTipodenunciaS, TxdDenunciaTipoS

@api_view(['GET', 'POST'])
def lista_objetos(request):
    """
    Lista de todos los Tipodenuncias, o crea uno nuevo.
    """

    if request.method == 'GET':
        objeto = TxdTipodenuncia.objects.all()
        serializador = TxdDenunciaTipoS(objeto, many=True)
        return Response(serializador.data)

    elif request.method == 'POST':
        serializador = TxdTipodenunciaS(data=request.data)
        if serializador.is_valid():
            serializador.save()
            return Response(serializador.data, status=status.HTTP_201_CREATED)
        return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def detalle_objetos(request, pk):
    """
    Actuliza, elimina un objeto segun su id
    """
    try:
        objeto = TxdTipodenuncia.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializador = TxdTipodenunciaS(objeto)
        return Response(serializador.data)

    elif request.method == 'PUT':
        serializador = TxdTipodenunciaS(objeto, data=request.data)
        if serializador.is_valid():
            serializador.save()
            return Response(serializador.data)
        return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        objeto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
