from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.models import TxcCultura
from app.serializables import TxcCulturaS
from app import permisos
from app.vistas import autentificacion

@api_view(['GET', 'POST'])
def lista_objetos(request, tk):
    """
    Lista de todos los usuarios de cultura, o crea uno nuevo.
    """
    usuario = autentificacion.autenticacion(tk)
    if usuario.has_perms(permisos.duenios):
        if request.method == 'GET':
            objeto = TxcCultura.objects.all()
            serializador = TxcCulturaS(objeto, many=True)
            return Response(serializador.data)

        elif request.method == 'POST':
            serializador = TxcCulturaS(data=request.data)
            if serializador.is_valid():
                serializador.save()
                return Response(serializador.data, status=status.HTTP_201_CREATED)
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)
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
            objeto = TxcCultura.objects.get(pk=pk)
        except objeto.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializador = TxcCulturaS(objeto)
            return Response(serializador.data)

        elif request.method == 'PUT':
            serializador = TxcCulturaS(objeto, data=request.data)
            if serializador.is_valid():
                serializador.save()
                return Response(serializador.data)
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            data = {"nombre": objeto.nombre ,"apellidos": objeto.apellidos,"direccion":objeto.direccion,
            "dpi":objeto.dpi, "telefono":objeto.telefono, "correo":objeto.correo,"foto":objeto.foto, "usuario_id":objeto.idusuario}
            data['estado']= 0
            print data
            serializador = TxcCulturaS(objeto,data=data)
            if serializador.is_valid():
                serializador.save()
                content = {'estado': 'se deshabilito'}
                return Response(content, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serializador.errors,status=status.HTTP_400_BAD_REQUEST)
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
            objeto = TxcCultura.objects.filter(usuario__isnull=True)
            serializador = TxcCulturaS(objeto, many=True)
            return Response(serializador.data)
        else:
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("No tiene los permisos necesarios", status=status.HTTP_403_NOT_FOUND)
