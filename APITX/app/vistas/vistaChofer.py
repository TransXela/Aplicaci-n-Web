from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.models import TxdChofer
from app.serializables import TxdChoferS, ChoferesDenuncias
from app import permisos

@api_view(['GET', 'POST'])
def lista_objetos(request):
    """
    Lista de todos los choferes, o crea uno nuevo
    """
    if request.user.has_perms(permisos.lista_duenios):
        if request.method == 'GET':
            objeto = TxdChofer.objects.all()
            serializador = TxdChoferS(objeto, many = true)
            return Response(serializador.data)

        elif request.method == 'POST':
            serializador = TxdChoferS(data = request.data)
            if serializador.is_valid():
                serializador.save()
                return Response(serializador.data, status=status.HTTP_201_CREATED)
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_403_NOT_FOUND)


@api_view(['GET', 'PUT', 'DELETE'])
def detalle_objetos(request, pk):
    """
    Actuliza o elimina o chofer segun su id
    """
    if request.user.has_perms(permisos.lista_duenios):
        try:
            objeto = TxdChofer.objects.get(pk=pk)
        except objeto.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializador = TxdChoferS(objeto)
            return Response(serializador.data)

        elif request.method == 'PUT':
            serializador = TxdChoferS(objeto, data=request.data)
            if serializador.is_valid():
                serializador.save()
                return Response(serializador.data)
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            objeto.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    else:
        return Response(status=status.HTTP_403_NOT_FOUND)

@api_view(['GET'])
def lista_choferes_denuncias(request):
    """
    Lista de todos los choferes con sus denuncias
    """
    if request.user.has_perms(permisos.lista_duenios):
        if request.method == 'GET':
            objeto = TxdChofer.objects.all()
            print objeto
            serializador = ChoferesDenuncias(objeto)
            return Response(serializador.data)
    else:
        return Response(status=status.HTTP_403_NOT_FOUND)
