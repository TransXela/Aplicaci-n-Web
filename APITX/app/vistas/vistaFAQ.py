from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from app.models import TxcPreguntaarticulo, TxcPregunta, TxcArticulo, TxcCapitulo, TxcTitulo
from app.serializables import TxcPreguntaarticuloS,TxcPreguntaS, TxcTituloS,TxcArticuloS,TxcCapituloS
from app.vistas import autentificacion
from app import permisos


@api_view(['GET', 'POST'])
def lista_objetos(request, pk, tk):

    """
    Lista de todas las actividades, o crear una nueva
    """
    usuario = autentificacion.autenticacion(tk)
    if usuario.has_perms(permisos.duenios):
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
    else:
        return Response("No tiene los permisos necesarios", status=status.HTTP_403_NOT_FOUND)
