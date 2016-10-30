"""APITX URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views
from app.vistas import (vistaDuenio, vistaRuta, vistaHorario, vistaDenuncia, vistaTipodenuncia, vistaActividad,vistaConsejo, vistaFechaConsejo,
                        vistaBus, vistaRecurso, vistaChofer, vistaHorariodetalle, vistaTipodenuncia, vistaCapitulo, vistaPregunta, vistaTitulo,
                        vistaArticulo, autenticacion, vistaUsuario, vistaPmt, vistaGrupoUsuario, vistaFAQ, vistaEstadistica)

from APITX import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'users', vistaGrupoUsuario.UserViewSet)
router.register(r'groups', vistaGrupoUsuario.GroupViewSet)

urlpatterns = [

    url(r'^token-auth/', views.obtain_auth_token),
    url(r'^admin/', admin.site.urls),
    url(r'^duenio/$', vistaDuenio.lista_objetos),
    url(r'^operador/duenios/$', vistaDuenio.lista_objetos),
    url(r'^admin/duenio/lista/$', vistaDuenio.lista_objetos),

    url(r'^duenio/(?P<pk>[0-9]+)$', vistaDuenio.detalle_objetos),
    url(r'^duenio/(?P<pk>[0-9]+)/principal/$', vistaDuenio.principal_duenio_choferes,{'var': 0}),
    url(r'^duenio/(?P<pk>[0-9]+)/pilotos/$', vistaDuenio.principal_duenio_choferes,{'var': 1}),

    #url(r'^duenio/(?P<pk>[0-9]+)/verhorarios/$', vistaDuenio.principal_duenio_choferes,{'var': 2}),
    url(r'^duenio/(?P<pk>[0-9]+)/buses/$', vistaDuenio.principal_duenio_choferes,{'var': 3}),

    url(r'^duenio/piloto/$', vistaChofer.lista_objetos),
    url(r'^duenio/piloto/(?P<pk>[0-9]+)$', vistaChofer.detalle_objetos),
    url(r'^duenio/piloto/(?P<pk>[0-9]+)/editar/$', vistaChofer.detalle_objetos),

    url(r'^duenio/bus/$', vistaBus.lista_objetos),
    #url(r'^duenio/bus/activos/$', vistaBus.buses_Activos),
    url(r'^duenio/bus/(?P<pk>[0-9]+)$', vistaBus.detalle_objetos),

    url(r'^duenio/horario/$', vistaHorario.lista_objetos),
    url(r'^duenio/horario/(?P<pk>[0-9]+)$', vistaHorario.detalle_objetos),
    url(r'^duenio/(?P<pk>[0-9]+)/horarios/$', vistaHorario.horarios_duenio),
    #url(r'^duenio/crear/horario/$', vistaHorario.crear_horario),

    url(r'^duenio/horariodetalle/$', vistaHorariodetalle.lista_objetos),
    url(r'^duenio/horariosdetalle/$', vistaHorariodetalle.lista_objetos), # obtiene todos los horarios y detalles
    url(r'^duenio/horariodetalle/(?P<fInicio>20[0-9][0-9]-[0-1][0-9]-[0-3][0-9])/(?P<fFin>20[0-9][0-9]-[0-1][0-9]-[0-3][0-9])$', vistaHorariodetalle.rango),

    #actualizar un horariodetalle PUT/DELETE
    url(r'^duenio/horariodetalle/(?P<pk>[0-9]+)$', vistaHorariodetalle.detalle_objetos),# Obtiene uno en especifico
    url(r'^duenio/(?P<pk>[0-9]+)/horariosdetalle/$', vistaHorariodetalle.lista_por_duenio),# Otiene el listado de horarios de un duenio

    url(r'^ruta/$', vistaRuta.lista_objetos),
    url(r'^ruta/(?P<pk>[0-9]+)$', vistaRuta.detalle_objetos),
    url(r'^duenio/bus/(?P<pk>[0-9]+)/editar/$', vistaBus.detalle_objetos),
    url(r'^recurso/$', vistaRecurso.lista_objetos),
    url(r'^recurso/(?P<pk>[0-9]+)$', vistaRecurso.detalle_objetos),

    #url denuncia para movil
    url(r'^denuncia/$', vistaDenuncia.lista_objetos,{'var': 0}),
    url(r'^denuncia/recursos$', vistaDenuncia.lista_objetos,{'var': 1}),
    url(r'^denuncia/recurso$', vistaRecurso.lista_objetos),
    url(r'^denuncia/detalle/$', vistaDenuncia.detalle_objetos,{'var': 0}),
    url(r'^denuncia/detalle/recursos/$', vistaDenuncia.detalle_objetos,{'var': 1}),
    url(r'^denuncia/tipo/$', vistaTipodenuncia.lista_objetos),
    url(r'^denuncia/tipo/(?P<pk>[0-9]+)$', vistaTipodenuncia.detalle_objetos),

    #para realizar reportes por duenios
    url(r'^duenio/RepDuenioBusD/$', vistaEstadistica.lista_objetos),

    url(r'^operador/denuncias/ruta/(?P<pk>[0-9]+)$', vistaDenuncia.detalle_objetos),
    url(r'^tipodenuncia/$', vistaTipodenuncia.lista_objetos),

    #horariodetalle
    url(r'^horariosdetalle/piloto/(?P<pk>[0-9]+)$', vistaHorariodetalle.detalle_Choferes),
    #url modulo PMT
    url(r'^pmt/(?P<pk>[0-9]+)$', vistaPmt.detalle_objetos),
    url(r'^pmt/duenio/$', vistaDuenio.lista_objetos),
    url(r'^pmt/duenio/(?P<pk>[0-9]+)$', vistaDuenio.detalle_objetos),
    url(r'^pmt/ruta/$', vistaRuta.lista_objetos),
    url(r'^pmt/rutas/$', vistaRuta.lista_objetos),
    url(r'^pmt/ruta/(?P<pk>[0-9]+)$', vistaRuta.detalle_objetos),
    url(r'^pmt/horario/$', vistaHorario.lista_objetos),
    url(r'^pmt/denuncias/pilotos/$', vistaChofer.lista_choferes_denuncias),
    url(r'^pmt/horariosdetalle/$', vistaDuenio.lista_horariodetalle),

    #endPoints sesion
    url(r'^sesion/$', vistaUsuario.crear_usuario),
    url(r'^sesion/log/$', vistaUsuario.autenticar),
    url(r'^sesion/(?P<pk>[0-9]+)/$', vistaUsuario.detalle_usuario),

    #operador
    #estos dendponts por algun motivo no aparecen !
    url(r'^piloto/(?P<pk>[0-9]+)$', vistaChofer.chofer_dpi),
    url(r'^bus/(?P<pk>[1-9a-zA-Z]+)$', vistaBus.bus_placa),
    url(r'^horariosdetalle/bus/(?P<pk>[1-9]+)/$', vistaHorariodetalle.lista_por_bus),
    url(r'^denuncias/$', vistaDenuncia.lista_denuncias),
    url(r'^denuncia/estado/(?P<pk>[0-9]+)$', vistaDenuncia.cambio_estado),
    url(r'^denuncias/ruta/(?P<pk>[0-9]+)$', vistaRuta.denuncias_ruta),

    #url(r'^tipodenuncia/(?P<pk>[0-9]+)$', vistaTipodenuncia.detalle_objetos),
    #url(r'^tipodiahorariodetalle/$', vistadiahorariodetalle.lista_objetos),
    #url(r'^tipodiahorariodetalle/(?P<pk>[0-9]+)$', vistadiahorariodetalle.detalle_objetos),
    ##url(r'^snippets/(?P<pk>[0-9]+)$', views.snippet_detail),
    url(r'^cultura/actividad/$', vistaActividad.lista_objetos),
    url(r'^cultura/actividad/(?P<pk>[0-9]+)$', vistaActividad.detalle_objetos),
    url(r'^cultura/actividad/(?P<busq>([2][0][1-9]{2}-([1-9]|[1][0-2])-([0][1-9]|[1-2][0-9]|[3][0-1]))|[1-9a-z\s]+[0-9a-z\s]*)$', vistaActividad.busqueda),
    url(r'^cultura/consejos/$', vistaFechaConsejo.lista_objetos),
    url(r'^cultura/consejo/$', vistaFechaConsejo.lista_objetos),
    url(r'^cultura/consejos/(?P<pk>[0-9]+)$', vistaFechaConsejo.detalle_objetos),
    url(r'^cultura/consejodeldia/$', vistaConsejo.lista_objetos),
    url(r'^cultura/capitulo/$', vistaCapitulo.lista_objetos),
    url(r'^cultura/capitulo/(?P<pk>[0-9]+)$', vistaCapitulo.detalle_objetos),
    url(r'^cultura/pregunta/$',vistaPregunta.lista_objetos),
    url(r'^cultura/pregunta/(?P<pk>[0-9]+)$',vistaPregunta.detalle_objetos),
    url(r'^cultura/titulo/$',vistaTitulo.lista_objetos),
    url(r'^cultura/titulo/(?P<pk>[0-9]+)$', vistaTitulo.detalle_objetos),
    url(r'^cultura/articulo/$', vistaArticulo.lista_objetos),
    url(r'^cultura/articulo/(?P<pk>[0-9]+)$', vistaArticulo.detalle_objetos),
    url(r'^cultura/preguntas/(?P<pk>[0-9]+)$', vistaFAQ.lista_objetos),

    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
