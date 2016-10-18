from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.models import TxcActividad
from app.serializables import TxcActividadS


@api_view(['GET', 'POST'])
def lista_objetos(request):
    """
    Lista de todas las actividades, o crear una nueva
    """
    if request.method == 'GET':
        objeto = TxcActividad.objects.all()
        serializador = TxcActividadS(objeto, many=True)
        return Response(serializador.data)

    elif request.method == 'POST':
        serializador = TxcActividadS(data=request.data)
        if serializador.is_valid():
            serializador.save()
            return Response(serializador.data,status=status.HTTP_201_CREATED)
            return Response(serializador.errors,status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET', 'PUT','DELETE'])
def detalle_objetos(request, pk):
    """
    Actualiza, elimina un objeto segun su id
    """
    try:
        objeto = TxcActividad.objects.get(pk=pk)
    except objeto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializador = TxcActividadS(objeto)
        return Response(serializador.data)

    elif request.method == 'PUT':
        serializador = TxcActividadS(objeto, data=request.data)
        if serializador.is_valid():
            serializador.save()
            return Response(serializador.data)
        return Response(serializador.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        #objeto.delete()
        data = {
        "nombre": objeto.nombre,
        "descripcion": objeto.descripcion,
        "fecha": objeto.fecha,
        "lugar": objeto.lugar,
        "latitud": objeto.latitud,
        "longitud": objeto.longitud,
        "direccion": objeto.direccion,
        }
        data['estado']=0
        print data
        serializador = TxcActividadS(objeto, data=data)
        if serializador.is_valid():
            serializador.save()
            content = {'estado': 'se deshabilito'}
            return Response(content, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def busqueda(request, busq):
    try:
        objeto = TxcActividad.objects.filter(nombre__contains=busq) | TxcActividad.objects.filter(lugar__contains=busq) | TxcActividad.objects.filter(fecha__contains=busq)
    except objeto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializador = TxcActividadS(objeto, many=True)
        return Response(serializador.data)
