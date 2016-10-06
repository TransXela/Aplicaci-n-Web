from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.models import TxdBus
from app.serializables import TxdBusS


@api_view(['GET', 'POST'])
def lista_objetos(request):
    """
    Lista de todas las Buses, o crear una nueva
    """
    if request.method == 'GET':
        todos = request.META.get('todos')
        if todos:
            objeto = TxdBus.objects.all()
        else:
            objeto = TxdBus.objects.all(estado=1)

        serializador = TxdBusS(objeto, many=True)
        return Response(serializador.data)

    elif request.method == 'POST':
        serializador = TxdBusS(data=request.data)
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
        objeto = TxdBus.objects.get(pk=pk)
    except objeto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializador = TxdBusS(objeto)
        return Response(serializador.data)

    elif request.method == 'PUT':
        serializador = TxdBusS(objeto, data=request.data)
        if serializador.is_valid():
            serializador.save()
            return Response(serializador.data)
        return Response(serializador.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        objeto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
