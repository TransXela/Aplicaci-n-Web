from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, date
from app.models import TxdHorariodetalle,TxdBus,TxdChofer
from app.serializables import TxdHorariodetalleS


@api_view(['GET', 'POST'])
def lista_objetos(request):
    """
    Lista de todos los Horariodetalles, o crea uno nuevo.
    """
    if request.method == 'GET':
        objeto = TxdHorariodetalle.objects.all()
        serializador = TxdHorariodetalleS(objeto, many=True)
        return Response(serializador.data)

    elif request.method == 'POST':

        serializador = TxdHorariodetalleS(data=request.data)
        if serializador.is_valid():
            try:
                chofer = TxdChofer.objects.get(pk=request.data['chofer'],estado=1)
            except ObjectDoesNotExist:
                respuesta ={'crear': {'estado': 'No puede asignar un piloto deshabilitado.'}}
                return Response(respuesta, status=status.HTTP_406_NOT_ACCEPTABLE)

            try:
                bus = TxdBus.objects.get(pk=request.data['bus'], estado=1)
            except ObjectDoesNotExist:
                respuesta ={'crear': {'estado": "No puede asignar un bus deshabilitado.'}}
                return Response(respuesta, status=status.HTTP_406_NOT_ACCEPTABLE)

            formato_fecha = "%Y-%m-%d"
            fecha2 = datetime.strptime(request.data['fecha'], formato_fecha)
            stringF=str(datetime.now().year)+"-"+str(datetime.now().month)+"-"+str(datetime.now().day)
            fecha1 = datetime.strptime(stringF, formato_fecha)
            if fecha2 < fecha1:
                respuesta ={'crear': {'estado": "La fecha debe ser mayor igual a la fecha actual.'}}
                return Response(respuesta, status=status.HTTP_406_NOT_ACCEPTABLE)
            serializador.save()
            respuesta ={'crear': {'estado": "Creado Exitosamente'}}
            return Response(respuesta, status=status.HTTP_201_CREATED)
        return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def detalle_objetos(request, pk):
    """
    Actuliza, elimina un objeto segun su id
    """
    try:
        objeto = TxdHorariodetalle.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(serializador.data)
        serializador = TxdHorariodetalleS(objeto)

    elif request.method == 'PUT':
        serializador = TxdHorariodetalleS(objeto, data=request.data)
        if serializador.is_valid():
            try:
                chofer = TxdChofer.objects.get(pk=request.data['chofer'],estado=1)
            except ObjectDoesNotExist:
                respuesta ={'modificar': {'estado': 'No puede asignar un piloto deshabilitado.'}}
                return Response(respuesta, status=status.HTTP_406_NOT_ACCEPTABLE)

            try:
                bus = TxdBus.objects.get(pk=request.data['bus'], estado=1)
            except ObjectDoesNotExist:
                respuesta ={'modificar': {'estado": "No puede asignar un bus deshabilitado.'}}
                return Response(respuesta, status=status.HTTP_406_NOT_ACCEPTABLE)

            formato_fecha = "%Y-%m-%d"
            fecha2 = datetime.strptime(request.data['fecha'], formato_fecha)
            stringF=str(datetime.now().year)+"-"+str(datetime.now().month)+"-"+str(datetime.now().day)
            fecha1 = datetime.strptime(stringF, formato_fecha)
            if fecha2 < fecha1:
                respuesta ={'modificar': {'estado": "La fecha debe ser mayor igual a la fecha actual.'}}
                return Response(respuesta, status=status.HTTP_406_NOT_ACCEPTABLE)
            serializador.save()
            respuesta ={'modificar': {'estado": "Modificado Exitosamente'}}
            return Response(respuesta, status=status.HTTP_202_ACCEPTED)
        return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        formato_fecha = "%Y-%m-%d"
        fecha2 = datetime.combine(objeto.fecha,  datetime.min.time())
        stringF=str(datetime.now().year)+"-"+str(datetime.now().month)+"-"+str(datetime.now().day)
        fecha1 = datetime.strptime(stringF, formato_fecha)

        if fecha2 >= fecha1:
            objeto.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            data = request.data
            data['estado']= 0
            serializador = TxdHorariodetalleS(data=data)
            serializador.save
            content = {'estado': 'se deshabilito'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
            #respuesta ={'eliminar': {'estado": "no puede eliminar un registro con una fecha anterior a la actual.'}}
            #return Response(respuesta, status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['GET'])
def rango(request,fInicio,fFin):
    """
    Actuliza, elimina un objeto segun su id
    """
    formato_fecha = "%Y-%m-%d"
    inicio = datetime.strptime(fInicio, formato_fecha).date()
    fin = datetime.strptime(fFin, formato_fecha).date()

    try:
        hoy = date.today()
        objeto = TxdHorariodetalle.objects.filter(bus=1)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializador = TxdHorariodetalleS(objeto)
        return Response(serializador.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
