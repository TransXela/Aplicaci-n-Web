from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import IntegrityError
from app.models import TxdRuta,TxdDenuncia,TxdBus, TxdHorariodetalle
from app.serializables import TxdRutaS, TxdDenunciaS,TxdBusS
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

@api_view(['GET', 'POST'])
def lista_objetos(request):
    """
    Lista de todos los Rutas, o crea uno nuevo.
    """
    try:
        objToken = Token.objects.get(key=request.query_params.get('tk'))
        usuario = User.objects.get(pk=objToken.user.id)
    except ObjectDoesNotExist:
        content = {'Datos incorrectos': 'El token enviado no coincide para ningun usuario'}
        return Response(content, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        if usuario.has_perm('app.view_txdruta'):
            objeto = TxdRuta.objects.all()
            serializador = TxdRutaS(objeto, many=True)
            return Response(serializador.data)
        else:
            content = {'Permiso denegado': 'El usuario no tiene permisos para ver los datos'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)

    elif request.method == 'POST':
        if usuario.has_perm('app.add_txdruta'):
            serializador = TxdRutaS(data=request.data)
            if serializador.is_valid():
                serializador.save()
                return Response(serializador.data, status=status.HTTP_201_CREATED)
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            content = {'Permiso denegado': 'El usuario no tiene permisos para ingresar datos'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)


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
        objeto = TxdRuta.objects.get(pk=pk)
    except objeto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        if usuario.has_perm('app.view_txdruta'):
            serializador = TxdRutaS(objeto)
            return Response(serializador.data)
        else:
            content = {'Permiso denegado': 'El usuario no tiene permisos para ver los datos'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)

    elif request.method == 'PUT':
        if usuario.has_perm('app.change_txdruta'):
            serializador = TxdRutaS(objeto, data=request.data)
            if serializador.is_valid():
                serializador.save()
                return Response(serializador.data)
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            content = {'Permiso denegado': 'El usuario no tiene permisos para editar datos'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)


    elif request.method == 'DELETE':
        if usuario.has_perm('app.delete_txdruta'):
            try:
                objeto.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except IntegrityError:
                content = {'estado': 'No se puede eliminar tiene dependencias'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            content = {'Permiso denegado': 'El usuario no tiene permisos para eliminar datos'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
def denuncias_ruta(request, pk):
    """
    Lista de Denuncias de una ruta
    """
    try:
        objToken = Token.objects.get(key=request.query_params.get('tk'))
        usuario = User.objects.get(pk=objToken.user.id)
    except ObjectDoesNotExist:
        content = {'Datos incorrectos': 'El token enviado no coincide para ningun usuario'}
        return Response(content, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        if usuario.has_perm('app.view_txdruta'):
            try:
                ruta = TxdRuta.objects.get(pk=pk)
                denuncias = TxdDenuncia.objects.all()
                respuesta = {}
                listadenuncias = list()
                listaruta = list()
                listaruta+= [TxdRutaS(ruta).data]
            except ruta.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            for bus in TxdBus.objects.filter(ruta_id=ruta.idruta):
                try:
                    denuncias = TxdDenuncia.objects.filter(placa=bus.placa)
                    numdenuncias = TxdDenuncia.objects.filter(placa=bus.placa).count()
                    buses = TxdBusS(bus).data
                    buses['numdenuncias'] = numdenuncias
                    listadenuncias+= [buses]
                except denuncias.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            respuesta['ruta'] =  listaruta
            respuesta['buses'] = listadenuncias
            return Response(respuesta)
        else:
            content = {'Permiso denegado': 'El usuario no tiene permisos para ver los datos'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
def lista_numDenuncias(request):
    """
    Lista de todos los Rutas, o crea uno nuevo.
    """
    try:
        objToken = Token.objects.get(key=request.query_params.get('tk'))
        usuario = User.objects.get(pk=objToken.user.id)
    except ObjectDoesNotExist:
        content = {'Datos incorrectos': 'El token enviado no coincide para ningun usuario'}
        return Response(content, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        if usuario.has_perm('app.view_txdruta'):
            objeto = TxdRuta.objects.all()
            a= list()
            for ruta in objeto:
                cant = 0
                buses = TxdBus.objects.filter(ruta=ruta.idruta)
                for bus in buses:
                    cant+= TxdDenuncia.objects.filter(placa=bus.placa,chofer__isnull=False).count()
                ob={}
                ob={"idruta":ruta.idruta, "nombre":ruta.nombre, "recorrido":ruta.recorrido, "TotalDenuncias":cant}
                a+=[ob]
            rutas={}
            rutas['rutas'] = a
            return Response(rutas)
        else:
            content = {'Permiso denegado': 'El usuario no tiene permisos para ver los datos'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
