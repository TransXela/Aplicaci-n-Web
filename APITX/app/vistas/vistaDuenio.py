from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from app.models import TxdDuenio, TxdChofer, TxdHorario, TxdBus, TxdHorariodetalle
from app.serializables import (TxdDuenioS, TxdHorariodetalleS, DueniosChoferBuses, DueniosChoferes, DueniosHorarios, DueniosBuses,
                                listadoDueniosDetalles)
from app import permisos
from app.vistas import autentificacion
from django.core.exceptions import ObjectDoesNotExist

@api_view(['GET', 'POST'])
def lista_objetos(request):
    """
    Lista de todos los Duenios, o crea uno nuevo.
    """
    try:
        objToken = Token.objects.get(key=request.query_params.get('tk'))
        usuario = User.objects.get(pk=objToken.user.id)
    except ObjectDoesNotExist:
        content = {'Datos incorrectos': 'El token enviado no coincide para ningun usuario'}
        return Response(content, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        objeto = TxdDuenio.objects.all()
        serializador = TxdDuenioS(objeto, many=True)
        return Response(serializador.data)

    elif request.method == 'POST':
        if usuario.has_perm('app.add_txdduenio'):
            serializador = TxdDuenioS(data=request.data)
            if serializador.is_valid():
                serializador.save()
                return Response(serializador.data, status=status.HTTP_201_CREATED)
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            content = {'Permiso denegado': 'El usuario no tiene permisos para ingresar datos'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def principal_duenio_choferes(request,pk, var):
    """
    Lista los buses y choferes
    """
    try:
        objToken = Token.objects.get(key=request.query_params.get('tk'))
        usuario = User.objects.get(pk=objToken.user.id)
    except ObjectDoesNotExist:
        content = {'Datos incorrectos': 'El token enviado no coincide para ningun usuario'}
        return Response(content, status=status.HTTP_403_FORBIDDEN)

    try:
        objeto = TxdDuenio.objects.get(pk=pk)
    except ObjectDoesNotExist:
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
        objToken = Token.objects.get(key=request.query_params.get('tk'))
        usuario = User.objects.get(pk=objToken.user.id)
    except ObjectDoesNotExist:
        content = {'Datos incorrectos': 'El token enviado no coincide para ningun usuario'}
        return Response(content, status=status.HTTP_403_FORBIDDEN)

    try:
        objeto = TxdDuenio.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializador = TxdDuenioS(objeto)
        return Response(serializador.data)

    elif request.method == 'PUT':
        if usuario.has_perm('app.change_txdduenio'):
            serializador = TxdDuenioS(objeto, data=request.data)
            if serializador.is_valid():
                serializador.save()
                return Response(serializador.data)
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            content = {'Permiso denegado': 'El usuario no tiene permisos para editar datos'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)


    elif request.method == 'DELETE':
        if usuario.has_perm('app.delete_txdduenio'):
            data = {"nombre": objeto.nombre ,"apellidos": objeto.apellidos,"direccion":objeto.direccion,
            "empresa":objeto.empresa,"fecha_nac":objeto.fecha_nac,"fecha_crea":objeto.fecha_crea,
            "dpi":objeto.dpi, "telefono":objeto.telefono, "correo":objeto.correo,"foto":objeto.foto}
            data['estado']= 0
            serializador = TxdDuenioS(objeto,data=data)
            if serializador.is_valid():
                serializador.save()
                content = {'estado': 'se deshabilito'}
                return Response(content, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serializador.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            content = {'Permiso denegado': 'El usuario no tiene permisos para eliminar datos'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def lista_horariodetalle(request):
    """
    obtiene la lista de duenio
    """
    try:
        objToken = Token.objects.get(key=request.query_params.get('tk'))
        usuario = User.objects.get(pk=objToken.user.id)
    except ObjectDoesNotExist:
        content = {'Datos incorrectos': 'El token enviado no coincide para ningun usuario'}
        return Response(content, status=status.HTTP_403_FORBIDDEN)

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

@api_view(['GET'])
def obtener_sinUser(request):
    """
    Lista de todos los Duenios, o crea uno nuevo.
    """
    try:
        objToken = Token.objects.get(key=request.query_params.get('tk'))
        usuario = User.objects.get(pk=objToken.user.id)
    except ObjectDoesNotExist:
        content = {'Datos incorrectos': 'El token enviado no coincide para ningun usuario'}
        return Response(content, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        objeto = TxdDuenio.objects.filter(usuario__isnull=True)
        serializador = TxdDuenioS(objeto, many=True)
        return Response(serializador.data)
    else:
        return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)
