from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.models import TxdDenuncia
from app.serializables import TxdDenunciaS

@api_view(['GET'])
def lista_objetos(request):

    """
    Lista todas las denuncias
    """
    if request.method == 'GET':
        objeto = TxdDenuncia.objects.all()
        serializador = TxdDenunciaS(objeto, many=True)
        return Response(serializador.data)
