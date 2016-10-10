from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import hashlib
from datetime import datetime, date
from django.core.exceptions import ObjectDoesNotExist
from app.models import TxdDenuncia,TxdBus,TxdHorariodetalle,TxdToken
from app.serializables import TxdDenunciaS, TxdDenunciaRecursosS,TxdTokenS

@api_view(['POST'])
def obtenerToken(request):
    if request.method == 'POST':
        dato=request.data['imei']
        h = hashlib.new("sha1", dato)
        token ={"token":h.hexdigest()}
        serializador = TxdTokenS(data=token)
        if serializador.is_valid():
            serializador.save()
            return Response(token, status=status.HTTP_201_CREATED)
        else:
            respuesta ={'token': {'estado': 'rechazada'}}
            return Response(respuesta, status=status.HTTP_400_BAD_REQUEST)

def validar(token):
    try:
        token =TxdToken.objects.get(token=token)
        denuncias = TxdDenuncia.objects.filter(token=token.idtoken)
        print denuncias
        return True
    except ObjectDoesNotExist:
        return False


@api_view(['GET', 'POST'])
def lista_objetos(request, var):
    """
    Lista de todos los Denuncias, o crea uno nuevo.
    """

    if request.method == 'GET':
        print validar(request.GET['token'])
        objeto = TxdDenuncia.objects.all()
        serializador = TxdDenunciaS(objeto, many=True)
        if var==1:
            serializador = TxdDenunciaRecursosS(objeto, many=True)

        return Response(serializador.data)

    elif request.method == 'POST':


        try:
            placa = request.data['placa']
            bus = TxdBus.objects.get(placa=placa)
            data= {"placa": request.data['placa'] ,"idhash": request.data['idhash'],
            "descripcion": request.data['descripcion'] ,"tipodenuncia": request.data['tipodenuncia'],
            "estado": 1  ,"chofer": "" , "fechahora": datetime.now()}
        except ObjectDoesNotExist:
            data= {"placa": request.data['placa'] ,"idhash": request.data['idhash'],
            "descripcion": request.data['descripcion'] ,"tipodenuncia": request.data['tipodenuncia'],
            "estado": 2  ,"chofer": "" , "fechahora": datetime.now()}


        try:
            horario = TxdHorariodetalle.objects.get(bus=bus.idbus, fecha=date.today())
            data= {"placa": request.data['placa'] ,"idhash": request.data['idhash'],
            "descripcion": request.data['descripcion'] ,"tipodenuncia": request.data['tipodenuncia'],
            "estado": 1  ,"chofer": horario.chofer.idchofer, "fechahora": datetime.now()}
            serializador = TxdDenunciaS(data=data)
        except ObjectDoesNotExist:
            serializador = TxdDenunciaS(data=data)


        if serializador.is_valid():

            serializador.save()
            if data['estado']==1 :
                ultimoId = TxdDenuncia.objects.latest('iddenuncia')
                respuesta ={'denuncia': {'estado': 'aceptada y en proceso', "id": ultimoId.iddenuncia}}
                return Response(respuesta, status=status.HTTP_201_CREATED)
            else:
                respuesta ={'denuncia': {'estado': 'rechazada'}}
                return Response(respuesta, status=status.HTTP_400_BAD_REQUEST)


        return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def detalle_objetos(request, pk,var):
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
        if var==1:
            serializador = TxdDenunciaRecursosS(objeto)

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
