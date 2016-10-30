from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.models import TxdDenuncia, TxdBus, TxdRuta, TxdChofer, TxdDuenio
from app.serializables import TxdDenunciaS, BusRutaS, ChoferDenunciaS, BusDuenioS
from app.vistas import autentificacion
from app import permisos

@api_view(['GET'])
def lista_objetos(request, tk):

    """
    Lista todas las denuncias
    """
    usuario = autentificacion.autenticacion(tk)
    if usuario.has_perms(permisos.lista_duenios):
        if request.method == 'GET':
            objeto = TxdDenuncia.objects.all()
            serializador = TxdDenunciaS(objeto, many=True)
            return Response(serializador.data)
    else:
        return Response("No tiene los permisos necesarios", status=status.HTTP_403_NOT_FOUND)

@api_view(['GET'])
def lista_objetos_rutaBus(request, tk):

    """
    Lista todos las rutas y buses
    """
    usuario = autentificacion.autenticacion(tk)
    if usuario.has_perms(permisos.lista_duenios):
        if request.method == 'GET':
            objeto = TxdRuta.objects.all()
            serializador = BusRutaS(objeto, many=True)
            return Response(serializador.data)
    else:
        return Response("No tiene los permisos necesarios", status=status.HTTP_403_NOT_FOUND)

@api_view(['GET'])
def lista_objetos_pilotoDenuncia(request, tk):

    """
    Lista todos las rutas y buses
    """
    usuario = autentificacion.autenticacion(tk)
    if usuario.has_perms(permisos.lista_duenios):
        if request.method == 'GET':
            objeto = TxdChofer.objects.all()
            serializador = ChoferDenunciaS(objeto, many=True)
            return Response(serializador.data)
    else:
        return Response("No tiene los permisos necesarios", status=status.HTTP_403_NOT_FOUND)

@api_view(['GET'])
def lista_objetos_duenioBuses(request, tk):

    """
    Lista todos los buses de un duenio
    """
    usuario = autentificacion.autenticacion(tk)
    if usuario.has_perms(permisos.lista_duenios):
        if request.method == 'GET':
            objeto = TxdDuenio.objects.all()
            serializador = BusDuenioS(objeto, many=True)
            return Response(serializador.data)
    else:
        return Response("No tiene los permisos necesarios", status=status.HTTP_403_NOT_FOUND)
