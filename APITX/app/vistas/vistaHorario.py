from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from app.models import TxdHorario
from app.serializables import TxdHorarioS


@api_view(['GET', 'POST'])
def lista_objetos(request):
    """
    Lista de todos los Horarios, o crea uno nuevo.
    """
    if request.method == 'GET':
        objeto = TxdHorario.objects.all()
        serializador = TxdHorarioS(objeto, many=True)
        return Response(serializador.data)

    elif request.method == 'POST':
        serializador = TxdHorarioS(data=request.data)
        if serializador.is_valid():
            serializador.save()
            return Response(serializador.data, status=status.HTTP_201_CREATED)
        return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def detalle_objetos(request, pk):
    """
    Actuliza, elimina un objeto segun su id
    """
    try:
        objeto = TxdHorario.objects.get(pk=pk)
    except objeto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializador = TxdHorarioS(objeto)
        return Response(serializador.data)

    elif request.method == 'PUT':
        serializador = TxdHorarioS(objeto, data=request.data)
        if serializador.is_valid():
            serializador.save()
            return Response(serializador.data)
        return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        objeto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def crear_horario(request):
    """
    Crea un nuevo horario
    """
    if request.method == 'POST':
        serializador = TxdHorarioS(data=request.data)
        if serializador.is_valid():
            inicio = datetime.strptime(str(request.data.get('horainicio')),'%H:%M:%S')
            final = datetime.strptime(str(request.data.get('horafin')),'%H:%M:%S')
            if (final > inicio):
                serializador.save()
                respuesta ={"crear": {"estado": "Horario creado exitosamente"}}
                return Response(respuesta, status=status.HTTP_201_CREATED)
            else:
                respuesta ={"crear": {"estado": "El horario inicio debe ser menor/diferente a horario fin"}}
                return Response(respuesta, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def horarios_duenio(request, pk):
    """
    obtiene los horarios de un duenio
    """
    try:
        objeto = TxdHorario.objects.filter(duenio=pk)
    except objeto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializador = TxdHorarioS(objeto, many=True)
        return Response(serializador.data)
