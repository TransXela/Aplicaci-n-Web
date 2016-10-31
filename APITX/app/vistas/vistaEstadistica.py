from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.models import TxdDenuncia, TxdBus, TxdRuta, TxdChofer, TxdDuenio,TxdTipodenuncia
from app.serializables import TxdDenunciaS, BusRutaS, ChoferDenunciaS, BusDuenioS,PilotoDuenioS,TxdBusS, TxdTipodenunciaS,TipoDenDenunciaS

@api_view(['GET'])
def lista_objetos(request):

    """
    Lista todas las denuncias
    """
    if request.method == 'GET':
        objeto = TxdDenuncia.objects.all()
        serializador = TxdDenunciaS(objeto, many=True)
        return Response(serializador.data)

@api_view(['GET'])
def lista_objetos_rutaBus(request):

    """
    Lista todos las rutas y buses
    """
    if request.method == 'GET':
        objeto = TxdRuta.objects.all()
        serializador = BusRutaS(objeto, many=True)
        return Response(serializador.data)

@api_view(['GET'])
def lista_objetos_pilotoDenuncia(request):

    """
    Lista todos las rutas y buses
    """
    if request.method == 'GET':
        objeto = TxdChofer.objects.all()
        serializador = ChoferDenunciaS(objeto, many=True)
        return Response(serializador.data)

@api_view(['GET'])
def lista_objetos_duenioBuses(request):

    """
    Lista todos los buses de todos los duenios
    """
    if request.method == 'GET':
        objeto = TxdDuenio.objects.all()
        serializador = BusDuenioS(objeto, many=True)
        return Response(serializador.data)

@api_view(['GET'])
def lista_objetos_duenioBusesId(request, pk):

    """
    Lista todos los buses de un duenio por id
    """
    try:
        objeto = TxdDuenio.objects.get(pk=pk)
    except objeto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializador = BusDuenioS(objeto)
        return Response(serializador.data)

@api_view(['GET'])
def lista_objetos_duenioChofId(request, pk):

    """
    Lista todos los pilotos de un duenio por id
    """
    try:
        objeto = TxdDuenio.objects.get(pk=pk)
    except objeto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializador = PilotoDuenioS(objeto)
        return Response(serializador.data)

@api_view(['GET'])
def lista_objetos_busChofId(request, pk):

    """
    Lista todos los buses de un duenio por id
    """
    try:
        objeto = TxdBus.objects.filter(duenio=pk)
    except objeto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializador = TxdBusS(objeto, many=True)
        return Response(serializador.data)

@api_view(['GET'])
def lista_objetos_tipoDenDenuncia(request):

    """
    Lista todas las denuncias
    """
    if request.method == 'GET':
        objeto = TxdTipodenuncia.objects.all()
        serializador = TipoDenDenunciaS(objeto, many=True)
        return Response(serializador.data)
