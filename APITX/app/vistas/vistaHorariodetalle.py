from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, date
from app.models import TxdHorariodetalle,TxdBus,TxdChofer,TxdDuenio
from app.serializables import TxdHorariodetalleS,Duenios_horariodetalle,TxdDuenioS, choferHorariDetalle, TxdBusS
from app import permisos

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
            return Response(serializador.data, status=status.HTTP_201_CREATED)
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
        serializador = TxdHorariodetalleS(objeto)
        return Response(serializador.data)


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
            data = {"fecha": objeto.fecha ,"bus": objeto.bus.idbus,"chofer":objeto.chofer.idchofer,"horario":objeto.horario.idhorario}
            data['estado']= 0
            print data
            serializador = TxdHorariodetalleS(objeto,data=data)
            if serializador.is_valid():
                serializador.save()
                content = {'estado': 'se deshabilito'}
                return Response(content, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serializador.errors,status=status.HTTP_400_BAD_REQUEST)

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


@api_view(['GET'])
def lista_por_duenio(request,pk):
    """
    obtiene la lista de duenio
    """
    try:
        s =list()
        for i in TxdChofer.objects.filter(duenio=pk):
            s+=[i.idchofer]
        objeto =TxdHorariodetalle.objects.filter(chofer__in=s)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializador = Duenios_horariodetalle(objeto, many=True)
        duenio=TxdDuenio.objects.get(pk=pk)
        duenios = TxdDuenioS(duenio)
        data={"duenio":duenios.data,"diasHorarioDetalle": serializador.data}
        return Response(data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def detalle_Choferes(request, pk):
    """
    Actuliza, elimina un objeto segun su id
    """
    try:
        objeto = TxdChofer.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializador = choferHorariDetalle(objeto)
        return Response(serializador.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def lista_por_bus(request,pk):
    """
    obtiene la lista de horariodetalle por bus
    """
    try:
        objBus =TxdBus.objects.filter(pk=pk)
        objHorarioDetalle = TxdHorariodetalle.objects.filter(bus=pk)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serBus = TxdBusS(objBus, many=True)
        serHorarioDetalle = TxdHorariodetalleS(objHorarioDetalle, many = True)
        data={"Bus":serBus.data,"HorarioDetalle": serHorarioDetalle.data}
        return Response(data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
