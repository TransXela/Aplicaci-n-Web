from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import hashlib
from datetime import datetime, date,timedelta
from django.core.exceptions import ObjectDoesNotExist
from app.models import TxdDenuncia,TxdBus,TxdHorariodetalle,TxdToken
from app.serializables import TxdDenunciaS, TxdDenunciaRecursosS,TxdTokenS


def obtenerToken(imei):
    """
        Crea Tokens, para los dispositivos que deseen hacer denuncias
    """
    dato = imei
    h = hashlib.new("sha1", dato)
    token ={"token":h.hexdigest()}
    serializador = TxdTokenS(data=token)
    if serializador.is_valid():
        serializador.save()
        return token
    else:
        return

def validar(token):
    """
        Valida si el token tiene permisos y evaluar si puede realizar una consulta
    """
    try:
        token =TxdToken.objects.get(token=token)
        fecha = datetime.now()
        fecha2 = fecha-timedelta(hours=1)
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
        if 'HTTP_AUTHORIZATION' in request.META:
            token = request.META['HTTP_AUTHORIZATION']
            var2 = validar(token)
            var2['token']=False
            if var2['bolean']:
                token =TxdToken.objects.get(token=token)
                objeto = TxdDenuncia.objects.filter(token=token.idtoken)

                if var==0:
                    serializador = TxdDenunciaS(objeto, many=True)
                else:
                    serializador = TxdDenunciaRecursosS(objeto, many=True)

                return Response(serializador.data)
            else:
                return Response(var2['respuesta'], status=status.HTTP_400_BAD_REQUEST)
        else:
            respuesta ={'denuncia': {'estado': 'no envio el token'}}
            return Response(respuesta, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'POST':

        if 'HTTP_AUTHORIZATION' in request.META:
            token = request.META['HTTP_AUTHORIZATION']
            var = validar(token)
            var['token']=False
        else:
            if 'imei' in request.data:
                token = obtenerToken(request.data['imei'])['token']
                var ={'bolean':True, 'respuesta': {'estado': 'Si se hizo el token'},'token':True}
            else:
                var ={'bolean':False, 'respuesta': {'estado': 'No se efectuo la Denuncia, no tiene permisos'},'token':False}

        if var['bolean']:

            try:
                token =TxdToken.objects.get(token=token)
            except ObjectDoesNotExist:
                return Response( status=status.HTTP_400_BAD_REQUEST)
            busid=-1
            if 'placa' in request.data["denuncia"] and 'descripcion' in request.data["denuncia"] and 'tipodenuncia' in request.data["denuncia"] and 'latitud' in request.data["denuncia"] and 'longitud' in request.data["denuncia"]:
                data= {"placa": request.data['denuncia']['placa'] ,"idhash": '',
                "descripcion": request.data['denuncia']['descripcion'] ,"tipodenuncia": request.data['denuncia']['tipodenuncia'],
                "estado": ""  ,"chofer": "" , "fechahora": datetime.now(),"token": token.idtoken, "latitud":request.data['denuncia']['latitud'], "longitud":request.data['denuncia']['longitud']}
            else:
                respuesta ={'denuncia': {'estado': 'solicitud rechaza, no envio uno o mas parametros requeridos'}}
                serializador = TxdDenunciaS(data=request.data)
                serializador.is_valid()
                return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)

            try:
                bus = TxdBus.objects.get(placa=data['placa'])
                busid=bus.idbus
                idchofer= (TxdHorariodetalle.objects.get(bus=busid,fecha=date.today())).chofer.idchofer
                data['estado']= 1
                data['chofer']= idchofer
            except ObjectDoesNotExist:
                data['estado']= 2
                data['chofer']= ""


            serializador = TxdDenunciaS(data=data)
            if serializador.is_valid():

                serializador.save()
                ultimoId = TxdDenuncia.objects.latest('iddenuncia')
                if var['token']==False :
                    respuesta ={'denuncia': {'estado': 'en proceso', "id": ultimoId.iddenuncia}}
                    return Response(respuesta, status=status.HTTP_201_CREATED)
                else:
                    respuesta ={'denuncia': {'estado': 'en proceso', "id": ultimoId.iddenuncia,"token":token.token}}
                    return Response(respuesta, status=status.HTTP_201_CREATED)


            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(var['respuesta'], status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
def detalle_objetos(request, pk,var):
    """
    Actuliza, elimina un objeto segun su id
    """


    if request.method == 'GET':
        if 'HTTP_AUTHORIZATION' in request.META:
            token = request.META['HTTP_AUTHORIZATION']
            var2 = validar(token)
            var2['token']=False
            if var2['bolean']:
                try:
                    token =TxdToken.objects.get(token=token)
                    objeto = TxdDenuncia.objects.get(pk=pk,token=token.idtoken)
                    if var==0:
                        serializador = TxdDenunciaS(objeto)
                    else:
                        serializador = TxdDenunciaRecursosS(objeto)

                    return Response(serializador.data)
                except ObjectDoesNotExist:
                    respuesta ={'denuncia': {'estado': 'no tiene permiso para ver esta denuncia'}}
                    return Response(respuesta, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response(var2['respuesta'], status=status.HTTP_400_BAD_REQUEST)

        else:
            respuesta ={'denuncia': {'estado': 'no envio el token'}}
            return Response(respuesta, status=status.HTTP_400_BAD_REQUEST)


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
