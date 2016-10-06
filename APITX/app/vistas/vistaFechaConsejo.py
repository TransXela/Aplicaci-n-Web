from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.models import TxcoFecha
from app.serializables import TxcoFechaS


@api_view(['GET', 'POST'])
def lista_objetos(request):
    """
    Lista de todas las fechas de consejo, o crear uno nuevo
    """
    if request.method == 'GET':
        objeto = TxcoFecha.objects.all()
        serializador = TxcoFechaS(objeto, many=True)
        return Response(serializador.data)

    elif request.method == 'POST':
        serializador = TxcoFechaS(data=request.data)
        if serializador.is_valid():
            serializador.save()
            return Response(serializador.data,status=status.HTTP_201_CREATED)
            return Response(serializador.errors,status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET', 'PUT','DELETE'])
def detalle_objetos(request, pk):
    """
    Actualiza, elimina un objeto segun su id
    """
    try:
        objeto = TxcoFecha.objects.get(pk=pk)
    except objeto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializador = TxcoFechaS(objeto)
        return Response(serializador.data)

    elif request.method == 'PUT':
        serializador = TxcoFechaS(objeto, data=request.data)
        if serializador.is_valid():
            serializador.save()
            return Response(serializador.data)
        return Response(serializador.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        objeto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
