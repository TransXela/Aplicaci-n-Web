from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from app.models import TxdBus,TxdDenuncia, TxdTipodenuncia
from app.serializables import TxdBusS,TxdDenunciaS, TxdTipodenunciaS
from app import permisos

@api_view(['GET', 'POST'])
def lista_objetos(request):
    """
    Lista de todas las Buses, o crear una nueva
    """

    if request.method == 'GET':
        objeto = TxdBus.objects.all()
        serializador = TxdBusS(objeto, many=True)
        return Response(serializador.data)

    elif request.method == 'POST':
        serializador = TxdBusS(data=request.data)
        if serializador.is_valid():
            serializador.save()
            return Response(serializador.data, status=status.HTTP_201_CREATED)
        return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT','DELETE'])
def detalle_objetos(request, pk):
    """
    Actualiza, elimina un objeto segun su id
    """

    try:
        objeto = TxdBus.objects.get(pk=pk)
    except ObjectDoesNotExist:
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

@api_view(['GET'])
def buses_Activos(request):
    """
    retorna los busese que estan activos
    """
    try:
        objetos = TxdBus.objects.filter(estado=1)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializador = TxdBusS(objetos, many=True)
        return Response(serializador.data)

@api_view(['GET'])
def buses_Activos(request):
    """
    retorna los busese que estan activos
    """
    if request.user.has_perms(permisos.lista_duenios):
        try:
            objetos = TxdBus.objects.filter(estado=1)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializador = TxdBusS(objetos, many=True)
            return Response(serializador.data)
    else:
        return Response(status=status.HTTP_403_NOT_FOUND)

@api_view(['GET'])
def bus_placa(request, pk):
    """
    Busqueda de un bus segun placa
    """
    try:
        objeto = TxdBus.objects.get(placa=pk)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializador = TxdBusS(objeto)
        return Response(serializador.data)

@api_view(['GET'])
def denuncias_tipodenuncia(request, idB):
    """
    Filtro de Denuncias de un bus segun tipo de denuncia
    """
    respuesta = {}
    listatdenuncia = list()
    try:
        objeto = TxdBus.objects.get(idbus=idB)
        tiposdenuncias = TxdTipodenuncia.objects.all()
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        for tipodenuncia in tiposdenuncias:
            denunciasportipo = TxdDenuncia.objects.filter(tipodenuncia_id=tipodenuncia.idtipodenuncia) & TxdDenuncia.objects.filter(placa=objeto.placa)
            numdenuncias = denunciasportipo.count()
            if numdenuncias != 0:
                jsontipo = {"idtipoDenuncia":tipodenuncia.idtipodenuncia,"descripcion":tipodenuncia.descripcion, "NumeroDenuncias": numdenuncias}
                listatdenuncia+= [jsontipo]
        respuesta['bus'] = TxdBusS(objeto).data
        respuesta['TiposDenuncia'] = listatdenuncia
        return Response(respuesta)


@api_view(['GET'])
def denuncias_bus_tipodenuncia(request, idB,idTd):
    """
    Filtro de Denuncias de un bus segun tipo de denuncia
    """
    respuesta = {}
    lista = list()
    try:
        objeto = TxdBus.objects.get(idbus=idB)
        tipodenuncia = TxdTipodenuncia.objects.get(idtipodenuncia=idTd)
        denuncias = TxdDenuncia.objects.filter(tipodenuncia_id=idTd) & TxdDenuncia.objects.filter(placa=objeto.placa)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializador = TxdTipodenunciaS(tipodenuncia).data
        lista+= [serializador]
        respuesta['tipodenuncia'] = lista
        respuesta['denuncias'] = TxdDenunciaS(denuncias,many=True).data
        respuesta2 = {"tipodenuncia": respuesta['tipodenuncia']}, {"denuncias": respuesta['denuncias']}
        return Response(respuesta2)
