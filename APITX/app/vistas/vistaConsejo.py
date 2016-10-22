from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.models import TxcoConsejo
from app.serializables import TxcoConsejoS, TxcoFechaS, TxcoConsejosFechaS


@api_view(['GET', 'POST'])
def lista_objetos(request):
    """
    Lista de todas los consejos, o crear uno nuevo
    """
    if request.user.has_perms(permisos.lista_duenios):
        if request.method == 'GET':
            objeto = TxcoConsejo.objects.all()
            serializador = TxcoConsejosFechaS(objeto, many=True)
            return Response(serializador.data)

        elif request.method == 'POST':
            serializador = TxcoConsejoS(data=request.data)
            if serializador.is_valid():
                serializador.save()
                return Response(serializador.data,status=status.HTTP_201_CREATED)
            return Response(serializador.errors,status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_403_NOT_FOUND)


@api_view(['GET'])
def principal_consejo(request):
    """
    Lista de las fechas y consejos
    """
    if request.user.has_perms(permisos.lista_duenios):
        try:
            objeto = TxcoConsejo.objects.get(pk=pk)
        except objeto.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializador = ConsejosFecha(objeto, many=True)
            return Response(serializador.data)

        elif request.method == 'PUT':
            serializador = TxcoConsejoS(objeto, data=request.data)
            if serializador.is_valid():
                serializador.save()
                return Response(serializador.data)
            return Response(serializador.errors, statis=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            objeto.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_403_NOT_FOUND)


@api_view(['GET', 'PUT','DELETE'])
def detalle_objetos(request, pk):
    """
    Actualiza, elimina un objeto segun su id
    """
    if request.user.has_perms(permisos.lista_duenios):
        try:
            objeto = TxcoConsejo.objects.get(pk=pk)
        except objeto.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializador = TxcoConsejoS(objeto)
            return Response(serializador.data)

        elif request.method == 'PUT':
            serializador = TxcoConsejoS(objeto, data=request.data)
            if serializador.is_valid():
                serializador.save()
                return Response(serializador.data)
            return Response(serializador.errors,status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            objeto.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    else:
        return Response(status=status.HTTP_403_NOT_FOUND)
