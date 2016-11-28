from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.models import TxdDenuncia, TxdBus, TxdRuta, TxdChofer, TxdDuenio, TxdTipodenuncia
from app.serializables import TxdDenunciaS, BusRutaS, ChoferDenunciaS,TxdChoferS, BusDuenioS, PilotoDuenioS,TipoDenDenunciaS,TxdBusS, TxdDuenioS
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

"""
Listado de denuncias por chofer
"""
@api_view(['GET'])
def lista_busesDenunciadosChoferPmt(request):
    try:
        objToken = Token.objects.get(key=request.query_params.get('tk'))
        usuario = User.objects.get(pk=objToken.user.id)
    except ObjectDoesNotExist:
        content = {'Datos incorrectos': 'El token enviado no coincide para ningun usuario'}
        return Response(content, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        if usuario.has_perm('app.view_txdchofer'):
            vec = []
            cantidad = 0
            for recChof in TxdChofer.objects.all():
                serChof = TxdChoferS(recChof)
                for recDen in TxdDenuncia.objects.all():
                    serDen = TxdDenunciaS(recDen)
                    if recDen.chofer_id == recChof.idchofer:
                        cantidad=cantidad+1
                if cantidad>0:
                    var = {'dpi': recChof.dpi,'cantidad':cantidad}
                    vec+=[var]
                    cantidad = 0;
            return Response(vec)
        else:
            content = {'Persmiso Denegado':'El usuario no tiene Persmisos'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)

"""
lista de buses denunciados para PMT
"""
@api_view(['GET'])
def lista_busesDenunciadosPmt(request):
    if request.method == 'GET':
        try:
            objToken = Token.objects.get(key=request.query_params.get('tk'))
            usuario = User.objects.get(pk=objToken.user.id)
        except ObjectDoesNotExist:
            content = {'Datos incorrectos': 'El token enviado no coincide para ningun usuario'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        vec = []
        cantidad = 0
        if usuario.has_perm('app.view_txdbus'):
            for recBus in TxdBus.objects.all():
                serBus = TxdBusS(recBus)
                for recDen in TxdDenuncia.objects.all():
                    serDen = TxdDenunciaS(recDen)
                    if recBus.placa == recDen.placa:
                        cantidad=cantidad+1
                if cantidad > 0:
                    var = {'placa': recBus.placa, 'cantidad': cantidad}
                    vec+=[var]
                    cantidad=0
            return Response(vec)
        else:
            content = {'Permiso denagado': 'El usuario no tiene permisos'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)

"""
lista de los duenios denunciados para PMT
"""
@api_view(['GET'])
def lista_dueniosDenPmt(request):
    if request.method == 'GET':
        try:
            objToken = Token.objects.get(key=request.query_params.get('tk'))
            usuario = User.objects.get(pk=objToken.user.id)
        except ObjectDoesNotExist:
            content = {'Datos incorrectos': 'El token enviado no coincide para ningun usuario'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        cont = 0
        vec = []
        if usuario.has_perm('app.view_txdduenio'):
            for recD in TxdDuenio.objects.all():
                serD = TxdDuenioS(recD)
                for recB in TxdBus.objects.all():
                    serB = TxdBusS(recB)
                    if recD.idduenio == recB.duenio_id:
                        for recDen in TxdDenuncia.objects.all():
                            serDen = TxdDenunciaS(recDen)
                            if recB.placa == recDen.placa:
                                cont = cont + 1
                if cont > 0:
                    var = {'duenio': recD.idduenio, 'dpi': recD.dpi, 'cantidad': cont}
                    vec+=[var]
                cont = 0
            return Response(vec)
        else:
            content = {'Permiso denagado': 'El usuario no tiene permisos'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)


"""
lista de denuncias por tipo de denuncia para PMT
"""
@api_view(['GET'])
def lista_denunciasTipoDenPmt(request):
    if request.method == 'GET':
        try:
            objToken = Token.objects.get(key=request.query_params.get('tk'))
            usuario = User.objects.get(pk=objToken.user.id)
        except ObjectDoesNotExist:
            content = {'Datos incorrectos': 'El token enviado no coincide para ningun usuario'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        cont = 0
        vec = []
        if usuario.has_perm('app.view_txdtipodenuncia'):
            for recTD in TxdTipodenuncia.objects.all():
                for recD in TxdDenuncia.objects.all():
                    if recD.tipodenuncia_id == recTD.idtipodenuncia:
                        cont=cont+1
                if cont > 0:
                    var = {'tipo': recTD.descripcion, 'cant': cont}
                    vec += [var]
                cont = 0
            return Response(vec)
        else:
            content = {'Permiso denagado': 'El usuario no tiene permisos'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)

"""
lista de las rutas denunciadas para PMT
"""
@api_view(['GET'])
def lista_rutasDenPmt(request):
    if request.method == 'GET':
        try:
            objToken = Token.objects.get(key=request.query_params.get('tk'))
            usuario = User.objects.get(pk=objToken.user.id)
        except ObjectDoesNotExist:
            content = {'Datos incorrectos': 'El token enviado no coincide para ningun usuario'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        cont = 0
        vec = []
        if usuario.has_perm('app.view_txdruta'):
            for recR in TxdRuta.objects.all():
                for recB in TxdBus.objects.all():
                    if recR.idruta == recB.ruta_id:
                        for recD in TxdDenuncia.objects.all():
                            if recD.placa == recB.placa:
                                cont=cont+1
                if cont > 0:
                    var = {'ruta': recR.nombre, 'cant': cont}
                    vec += [var]
                cont = 0
            return Response(vec)
        else:
            content = {'Permiso denagado': 'El usuario no tiene permisos'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)

"""
DUENIO
lista de buses denunciados de un duenio
"""
@api_view(['GET'])
def lista_busesDenDuenio(request, pk):
    if request.method == 'GET':
        try:
            objToken = Token.objects.get(key=request.query_params.get('tk'))
            usuario = User.objects.get(pk=objToken.user.id)
        except ObjectDoesNotExist:
            content = {'Datos incorrectos': 'El token enviado no coincide para ningun usuario'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        cont = 0
        vec = []
        if usuario.has_perm('app.view_txdduenio'):
            obj = TxdDuenio.objects.get(pk=pk)
            for recB in TxdBus.objects.all():
                if recB.duenio_id == obj.idduenio:
                    for recD in TxdDenuncia.objects.all():
                        if recD.placa == recB.placa:
                            cont = cont + 1
                if cont > 0:
                    var = {'placa': recB.placa, 'cant': cont}
                    vec += [var]
                cont = 0
            return Response (vec)
        else:
            content = {'Permiso denagado': 'El usuario no tiene permisos'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
"""
DUENIO
listado de choferes denunciados por duenio
"""
@api_view(['GET'])
def lista_choferDenDuenio(request, pk):
    if request.method == 'GET':
        try:
            objToken = Token.objects.get(key=request.query_params.get('tk'))
            usuario = User.objects.get(pk=objToken.user.id)
        except ObjectDoesNotExist:
            content = {'Datos incorrectos': 'El token enviado no coincide para ningun usuario'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        cont = 0
        vec = []
        if usuario.has_perm('app.view_txdduenio'):
            obj = TxdDuenio.objects.get(pk=pk)
            for recC in TxdChofer.objects.all():
                if recC.duenio_id == obj.idduenio:
                    for recD in TxdDenuncia.objects.all():
                        if recD.chofer_id == recC.idchofer:
                            cont=cont+1
                if cont > 0:
                    var = {'dpi': recC.dpi, 'cant': cont}
                    vec += [var]
                cont = 0
            return Response (vec)
        else:
            content = {'Permiso denagado': 'El usuario no tiene permisos'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)

"""
DUENIO
lista de rutas denunciadas por duenios
"""
@api_view(['GET'])
def lista_rutasDenDuenio(request, pk):
    if request.method == 'GET':
        try:
            objToken = Token.objects.get(key=request.query_params.get('tk'))
            usuario = User.objects.get(pk=objToken.user.id)
        except ObjectDoesNotExist:
            content = {'Datos incorrectos': 'El token enviado no coincide para ningun usuario'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        vec = []
        cont = 0
        if usuario.has_perm('app.view_txdduenio'):
            objD = TxdDuenio.objects.get(pk=pk)
            for recR in TxdRuta.objects.all():
                for recB in TxdBus.objects.all():
                    if objD.idduenio == recB.duenio_id and recR.idruta == recB.ruta_id:
                        for recD in TxdDenuncia.objects.all():
                            if recD.placa == recB.placa:
                                cont = cont + 1
                if cont > 0:
                    var = {'ruta': recR.nombre, 'cant': cont}
                    vec +=[var]
                cont = 0
            return Response(vec)
        else:
            content = {'Permiso denagado': 'El usuario no tiene permisos'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)

"""
DUENIO
lista de denuncias por tipo de denuncia
"""
@api_view(['GET'])
def lista_tipoDenDuenio(request, pk):
    if request.method == 'GET':
        try:
            objToken = Token.objects.get(key=request.query_params.get('tk'))
            usuario = User.objects.get(pk=objToken.user.id)
        except ObjectDoesNotExist:
            content = {'Datos incorrectos': 'El token enviado no coincide para ningun usuario'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        vec = []
        cont = 0
        if usuario.has_perm('app.view_txdduenio'):
            objD = TxdDuenio.objects.get(pk=pk)
            for recT in TxdTipodenuncia.objects.all():
                for recD in TxdDenuncia.objects.all():
                    if recT.idtipodenuncia == recD.tipodenuncia_id:
                        for recB in TxdBus.objects.all():
                            if recB.duenio_id == objD.idduenio:
                                if recB.placa == recD.placa:
                                    cont = cont + 1
                if cont > 0:
                    var = {'tipo': recT.descripcion, 'cant': cont}
                    vec +=[var]
                cont = 0
            return Response(vec)
        else:
            content = {'Permiso denagado': 'El usuario no tiene permisos'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
