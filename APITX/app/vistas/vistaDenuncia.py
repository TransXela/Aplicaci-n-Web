from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime, date
from django.core.exceptions import ObjectDoesNotExist
from app.models import TxdDenuncia,TxdBus,TxdHorariodetalle
from app.serializables import TxdDenunciaS


@api_view(['GET', 'POST'])
def lista_objetos(request):
    """
    Lista de todos los Denuncias, o crea uno nuevo.
    """
    if request.method == 'GET':
        objeto = TxdDenuncia.objects.all()
        serializador = TxdDenunciaS(objeto, many=True)
        return Response(serializador.data)

    elif request.method == 'POST':

        try:
            placa = request.data['placa']
            bus = TxdBus.objects.get(placa=placa)
        except ObjectDoesNotExist:
            respuesta ={'denuncia': {'estado': 'rechazada'}}
            return Response(respuesta, status=status.HTTP_406_NOT_ACCEPTABLE)

        try:

            horario = TxdHorariodetalle.objects.get(bus=bus.idbus, fecha=date.today())
            data= {"placa": request.data['placa'] ,"idhash": request.data['idhash'],
            "descripcion": request.data['descripcion'] ,"tipodenuncia": request.data['tipodenuncia'],
            "estado": request.data['estado'] ,"chofer": horario.chofer.idchofer, "fechahora": request.data['fechahora']}
            serializador = TxdDenunciaS(data=data)
        except ObjectDoesNotExist:
            serializador = TxdDenunciaS(data=request.data)


        if serializador.is_valid():

            serializador.save()
            ultimoId = TxdDenuncia.objects.latest('iddenuncia')
            respuesta ={'denuncia': {'estado': 'aceptada', "id": ultimoId.iddenuncia}}
            return Response(respuesta, status=status.HTTP_201_CREATED)
        return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def detalle_objetos(request, pk):
    """
    Actuliza, elimina un objeto segun su id
    """
    try:
        objeto = TxdDenuncia.objects.get(pk=pk)
    except ObjectDoesNotExist:
        respuesta ={'denuncia': {'estado': 'no existe denuncia'}}
        return Response(respuesta,status=status.HTTP_204_NO_CONTENT)

    if request.method == 'GET':
        serializador = TxdDenunciaS(objeto)
        return Response(serializador.data)

    elif request.method == 'PUT':
        serializador = TxdDenunciaS(objeto, data=request.data)
        if serializador.is_valid():
            serializador.save()
            respuesta ={'denuncia': {'estado': 'se actualizo la denuncia'}}
            return Response(respuesta, status=status.HTTP_202_ACCEPTED)
        return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        objeto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
