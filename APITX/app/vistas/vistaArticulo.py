from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.models import TxcArticulo, TxcCapitulo
from app.serializables import TxcArticuloS, ArticuloCapituloS, TxcCapituloS


@api_view(['GET', 'POST'])
def lista_objetos(request):
    """
    Lista de todas las actividades, o crear una nueva
    """
    if request.user.has_perms(permisos.lista_duenios):
        if request.method == 'GET':
            objeto = TxcCapitulo.objects.all()
            serializador = ArticuloCapituloS(objeto, many=True)
            return Response(serializador.data)

        elif request.method == 'POST':
            serializador = TxcArticuloS(data=request.data)
            if serializador.is_valid():
                serializador.save()
                return Response(serializador.data,status=status.HTTP_201_CREATED)
                return Response(serializador.errors,status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_403_NOT_FOUND)


@api_view(['GET', 'PUT','DELETE'])
def detalle_objetos(request, pk):
    """
    Actualiza, elimina un objeto segun su id
    """
    if request.user.has_perms(permisos.lista_duenios):
        try:
            objeto = TxcArticulo.objects.get(pk=pk)
        except objeto.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializador = TxcArticuloS(objeto)
            return Response(serializador.data)

        elif request.method == 'PUT':
            serializador = TxcArticuloS(objeto, data=request.data)
            if serializador.is_valid():
                serializador.save()
                return Response(serializador.data)
            return Response(serializador.errors,status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            objeto.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_403_NOT_FOUND)
