from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from app.models import TxcPreguntaarticulo, TxcPregunta, TxcArticulo, TxcCapitulo, TxcTitulo
from app.serializables import TxcPreguntaarticuloS,TxcPreguntaS, TxcTituloS,TxcArticuloS,TxcCapituloS
from app.vistas import autentificacion
from app import permisos
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


@api_view(['GET'])
def lista_objetos(request, pk):

    """
    Lista de todas las actividades, o crear una nueva
    """
    try:
        objToken = Token.objects.get(key=request.query_params.get('tk'))
        usuario = User.objects.get(pk=objToken.user.id)
    except ObjectDoesNotExist:
        content = {'Datos incorrectos': 'El token enviado no coincide para ningun usuario'}
        return Response(content, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        try:
            todo=list()
            for x in TxcPregunta.objects.filter(pk=pk):
                preguntaSer=TxcPreguntaS(x)
                todo+=[preguntaSer.data]
                for y in TxcPreguntaarticulo.objects.filter(pregunta=x.idpregunta):
                    for z in TxcArticulo.objects.filter(pk=y.articulo.idarticulo):
                        articuloSer=TxcArticuloS(z)
                        todo+=[articuloSer.data]
                        for w in TxcCapitulo.objects.filter(pk=z.capitulo.idcapitulo):
                            capituloSer=TxcCapituloS(w)
                            todo+=[capituloSer.data]
                            for v in TxcTitulo.objects.filter(pk=w.titulo_0.idtitulo):
                                tituloSer=TxcTituloS(v)
                                todo+=[tituloSer.data]
            return Response(todo)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
