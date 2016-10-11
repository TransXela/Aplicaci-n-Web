from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import hashlib
from datetime import datetime, date,timedelta
from django.core.exceptions import ObjectDoesNotExist
from app.models import TxdDenuncia,TxdBus,TxdHorariodetalle,TxdToken
from app.serializables import TxdDenunciaS, TxdDenunciaRecursosS,TxdTokenS

@api_view(['POST'])
def obtenerToken(request):
    """
        Crea Tokens, para los dispositivos que deseen hacer denuncias
    """
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
    """
        Valida si el token tiene permisos y evaluar si puede realizar una consulta
    """
    try:
        fecha = datetime.now()
        fecha2 = fecha-timedelta(hours=1)
        token =TxdToken.objects.get(token=token)
        denuncias = TxdDenuncia.objects.filter(fechahora__range=(fecha2,fecha), token=token.idtoken)
        cantidad=len(denuncias)
        if cantidad <=2:
            respuesta ={'bolean':True, 'respuesta': {'estado': 'Puede hacer Denuncias'}}
            return respuesta
        else:
            respuesta ={'bolean':False, 'respuesta': {'estado': 'no tiene permitido hacer mas denuncias'}}
            return respuesta


    except ObjectDoesNotExist:
        respuesta ={'bolean':False, 'respuesta': {'estado': 'No tiene permisos'}}
        return respuesta


@api_view(['GET', 'POST'])
def lista_objetos(request, var):
    """
    Lista de todos los Denuncias, o crea uno nuevo.
    """

    if request.method == 'GET':

        objeto = TxdDenuncia.objects.all()
        serializador = TxdDenunciaS(objeto, many=True)
        if var==1:
            serializador = TxdDenunciaRecursosS(objeto, many=True)

        return Response(serializador.data)

    elif request.method == 'POST':

        var =  validar(request.GET['token'])

        if var['bolean']:

            try:
                token =TxdToken.objects.get(token=request.GET['token'])
            except ObjectDoesNotExist:
                return Response( status=status.HTTP_400_BAD_REQUEST)
            busid=-1
            if 'placa' in request.data and 'descripcion' in request.data and 'tipodenuncia' in request.data:
                data= {"placa": request.data['placa'] ,"idhash": '',
                "descripcion": request.data['descripcion'] ,"tipodenuncia": request.data['tipodenuncia'],
                "estado": ""  ,"chofer": "" , "fechahora": datetime.now(),"token": token.idtoken}
            else:
                respuesta ={'denuncia': {'estado': 'solicitud rechaza, no envio uno o mas parametros requeridos'}}
                return Response(respuesta, status=status.HTTP_400_BAD_REQUEST)

            try:
                bus = TxdBus.objects.get(placa=placa)
                busid=bus.idbus
                idchofer= (TxdHorariodetalle.objects.get(bus=busid,fecha=date.today())).chofer.idchofer
                data['estado']= 1
                data['chofer']= idchofer
            except ObjectDoesNotExist:
                data['estado']= 1
                data['chofer']= ""


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
        else:
            return Response(var['respuesta'], status=status.HTTP_400_BAD_REQUEST)



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
