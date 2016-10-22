from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.models import TxdDuenio, TxdChofer, TxdHorario, TxdBus, TxdHorariodetalle
from app.serializables import TxdDuenioS, DueniosChoferBuses, DueniosChoferes, DueniosHorarios, DueniosBuses, listadoDueniosDetalles


@api_view(['GET', 'POST'])
def lista_objetos(request):
    """
    Lista de todos los Duenios, o crea uno nuevo.
    """
    if request.method == 'GET':
        objeto = TxdDuenio.objects.all()
        serializador = TxdDuenioS(objeto, many=True)
        return Response(serializador.data)

    elif request.method == 'POST':
        serializador = TxdDuenioS(data=request.data)
        if serializador.is_valid():
            serializador.save()
            return Response(serializador.data, status=status.HTTP_201_CREATED)
        return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def principal_duenio_choferes(request,pk, var):
    """
    Lista los buses y choferes
    """
    try:
        objeto = TxdDuenio.objects.get(pk=pk)
    except objeto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        if var==0:

            serializador = TxdDuenioS(objeto)
            data = serializador.data
            data['no_Choferes']=len(TxdChofer.objects.filter(duenio=pk))
            data['no_Buses']=len(TxdBus.objects.filter(duenio=pk))
            data['no_Horarios']=len(TxdHorario.objects.filter(duenio=pk))
            return Response(data)
        elif var==1:
            serializador = DueniosChoferes(objeto)
            return Response(serializador.data)
        elif var==2:
            serializador = DueniosHorarios(objeto)
            return Response(serializador.data)
        elif var==3:
            serializador = DueniosBuses(objeto)
            return Response(serializador.data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PUT', 'DELETE'])
def detalle_objetos(request, pk):
    """
    Actuliza, elimina un objeto segun su id
    """
    try:
        objeto = TxdDuenio.objects.get(pk=pk)
    except objeto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializador = TxdDuenioS(objeto)
        return Response(serializador.data)

    elif request.method == 'PUT':
        serializador = TxdDuenioS(objeto, data=request.data)
        if serializador.is_valid():
            serializador.save()
            return Response(serializador.data)
        return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        data = {"nombre": objeto.nombre ,"apellidos": objeto.apellidos,"direccion":objeto.direccion,
        "empresa":objeto.empresa,"fecha_nac":objeto.fecha_nac,"fecha_crea":objeto.fecha_crea,
        "dpi":objeto.dpi, "telefono":objeto.telefono, "correo":objeto.correo,"foto":objeto.foto}
        data['estado']= 0
        print data
        serializador = TxdDuenioS(objeto,data=data)
        if serializador.is_valid():
            serializador.save()
            content = {'estado': 'se deshabilito'}
            return Response(content, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializador.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def lista_horariodetalle(request):
    """
    obtiene la lista de duenio
    """
    try:
        duenios = TxdDuenio.objects.all()
        horarios = TxdHorario.objects.all()
        detalleshorarios = TxdHorariodetalle.objects.all()
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        y = list()
        for duenio in duenios:
            s =list()
            a =list()
            #y+=[duenio.idduenio]
            y+=[duenio.nombre]
            for horario in TxdHorario.objects.filter(duenio=duenio.idduenio):
                s+=[horario.idhorario]
                for detallehorario in TxdHorariodetalle.objects.filter(horario=horario.idhorario):
                    y+=[detallehorario.idhorariodetalle]

                print y
        return Response(y)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
