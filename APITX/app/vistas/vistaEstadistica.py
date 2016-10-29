from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.models import TxdDenuncia, TxdBus, TxdRuta, TxdChofer
from app.serializables import TxdDenunciaS, BusRutaS, ChoferDenunciaS

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
