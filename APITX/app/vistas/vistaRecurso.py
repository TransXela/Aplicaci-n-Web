from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from app.models import TxdRecurso
from app.serializables import TxdRecursoS


@api_view(['GET', 'POST'])
def lista_objetos(request):
    """
    Lista de todas las Buses, o crear una nueva
    """
    if request.method == 'GET':
        objeto = TxdRecurso.objects.all()
        serializador = TxdRecursoS(objeto, many=True)
        return Response(serializador.data)

    elif request.method == 'POST':
        serializador = TxdRecursoS(data=request.data)
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
        objeto = TxdRecurso.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializador = TxdRecursoS(objeto)
        return Response(serializador.data)

    elif request.method == 'PUT':
        serializador = TxdRecursoS(objeto, data=request.data)
        if serializador.is_valid():
            serializador.save()
            return Response(serializador.data)
        return Response(serializador.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        objeto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
