from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.models import TxdDuenio, TxdChofer, TxdHorario, TxdBus, TxdHorariodetalle
from app.serializables import TxdDuenioS, TxdHorariodetalleS, DueniosChoferBuses, DueniosChoferes, DueniosHorarios, DueniosBuses, listadoDueniosDetalles
from app import permisos
from app.vistas import autentificacion

@api_view(['GET', 'POST'])
def lista_objetos(request, tk):
    """
    Lista de todos los Duenios, o crea uno nuevo.
    """
    usuario = autentificacion.autenticacion(tk)
    if usuario.has_perms(permisos.duenios):
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
    else:
        return Response("No tiene los permisos necesarios", status=status.HTTP_403_NOT_FOUND)

@api_view(['GET'])
def principal_duenio_choferes(request,pk, var, tk):
    """
    Lista los buses y choferes
    """
    usuario = autentificacion.autenticacion(tk)
    if usuario.has_perms(permisos.duenios):
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
    else:
        return Response("No tiene los permisos necesarios", status=status.HTTP_403_NOT_FOUND)

@api_view(['GET', 'PUT', 'DELETE'])
def detalle_objetos(request, pk, tk):
    """
    Actuliza, elimina un objeto segun su id
    """
    usuario = autentificacion.autenticacion(tk)
    if usuario.has_perms(permisos.duenios):
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
    else:
        return Response("No tiene los permisos necesarios", status=status.HTTP_403_NOT_FOUND)

@api_view(['GET'])
def lista_horariodetalle(request, tk):
    """
    obtiene la lista de duenio
    """
    usuario = autentificacion.autenticacion(tk)
    if usuario.has_perms(permisos.duenios):
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
                d=TxdDuenioS(duenio)
                ob={}
                ob['duenio']=d.data
                #y+=[duenio.idduenio]
                #y+=[duenio.nombre]
                for horario in TxdHorario.objects.filter(duenio=duenio.idduenio):
                    s+=[horario.idhorario]
                    detallehorario = TxdHorariodetalle.objects.filter(horario=horario.idhorario)
                    ob['detallehorarios']=TxdHorariodetalleS(detallehorario, many=True).data
                y+=[ob]
            return Response(y)
    else:
        return Response("No tiene los permisos necesarios", status=status.HTTP_403_NOT_FOUND)

@api_view(['GET'])
def obtener_sinUser(request, tk):
    """
    Lista de todos los Duenios, o crea uno nuevo.
    """
    usuario = autentificacion.autenticacion(tk)
    if usuario.has_perms(permisos.duenios):
        if request.method == 'GET':
            objeto = TxdDuenio.objects.filter(usuario__isnull=True)
            serializador = TxdDuenioS(objeto, many=True)
            return Response(serializador.data)
        else:
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("No tiene los permisos necesarios", status=status.HTTP_403_NOT_FOUND)
