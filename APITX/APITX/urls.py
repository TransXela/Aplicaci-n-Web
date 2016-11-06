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
from app.vistas import vistaGrupoUsuario
from app.vistas import (vistaDuenio, vistaRuta, vistaHorario, vistaDenuncia, vistaTipodenuncia, vistaActividad,vistaConsejo, vistaFechaConsejo,
                        vistaBus, vistaRecurso, vistaChofer, vistaHorariodetalle, vistaTipodenuncia, vistaCapitulo, vistaPregunta, vistaTitulo,
                        vistaArticulo, autenticacion, vistaUsuario, vistaPmt,vistaGrupo,vistaCultura,vistaEstadistica, autentificacion)
from APITX import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
#router.register(r'users', vistaGrupoUsuario.UserViewSet)
#router.register(r'groups', vistaGrupoUsuario.GroupViewSet)

urlpatterns = [

    url(r'^token-auth/', views.obtain_auth_token),
    url(r'^obtenertoken/', autentificacion.token),
    url(r'^admin/', admin.site.urls),
    url(r'^duenio/$', vistaDuenio.lista_objetos),
    url(r'^operador/duenios/(?P<tk>[0-9a-zA-Z]+)/$', vistaDuenio.lista_objetos),
    url(r'^admin/duenio/lista/(?P<tk>[0-9a-zA-Z]+)/$', vistaDuenio.lista_objetos),
    url(r'user/(?P<tk>[0-9a-zA-Z]+)/$', vistaGrupoUsuario.UserViewSet),

    url(r'^duenio/(?P<pk>[0-9]+)/(?P<tk>[0-9a-zA-Z]+)/$', vistaDuenio.detalle_objetos),
    url(r'^duenio/(?P<pk>[0-9]+)/principal/(?P<tk>[0-9a-zA-Z]+)/$', vistaDuenio.principal_duenio_choferes,{'var': 0}),
    url(r'^duenio/(?P<pk>[0-9]+)/pilotos/(?P<tk>[0-9a-zA-Z]+)/$', vistaDuenio.principal_duenio_choferes,{'var': 1}),
    url(r'^duenio/(?P<pk>[0-9]+)/buses/(?P<tk>[0-9a-zA-Z]+)/$', vistaDuenio.principal_duenio_choferes,{'var': 3}),
    url(r'^duenio/piloto/(?P<tk>[0-9a-zA-Z]+)/$', vistaChofer.lista_objetos),
    url(r'^duenio/piloto/(?P<pk>[0-9]+)/(?P<tk>[0-9a-zA-Z]+)/$', vistaChofer.detalle_objetos),
    url(r'^duenio/piloto/(?P<pk>[0-9]+)/editar/(?P<tk>[0-9a-zA-Z]+)/$', vistaChofer.detalle_objetos),
    url(r'^duenio/bus/(?P<tk>[0-9a-zA-Z]+)/$', vistaBus.lista_objetos),
    url(r'^duenio/bus/(?P<pk>[0-9]+)/(?P<tk>[0-9a-zA-Z]+)/$', vistaBus.detalle_objetos),
    url(r'^duenio/horario/(?P<tk>[0-9a-zA-Z]+)/$', vistaHorario.lista_objetos),
    url(r'^duenio/horario/(?P<pk>[0-9]+)/(?P<tk>[0-9a-zA-Z]+)/$', vistaHorario.detalle_objetos),
    url(r'^duenio/(?P<pk>[0-9]+)/horarios/(?P<tk>[0-9a-zA-Z]+)/$', vistaHorario.horarios_duenio),
    url(r'^duenio/horariodetalle/(?P<tk>[0-9a-zA-Z]+)/$', vistaHorariodetalle.lista_objetos),
    url(r'^duenio/horariosdetalle/(?P<tk>[0-9a-zA-Z]+)/$', vistaHorariodetalle.lista_objetos), # obtiene todos los horarios y detalles
    url(r'^duenio/horariodetalle/(?P<fInicio>20[0-9][0-9]-[0-1][0-9]-[0-3][0-9])/(?P<fFin>20[0-9][0-9]-[0-1][0-9]-[0-3][0-9])/(?P<tk>[0-9a-zA-Z]+)/$', vistaHorariodetalle.rango),
    url(r'^duenio/horariosdetalle/crearrango/(?P<tk>[0-9a-zA-Z]+)/$',vistaHorariodetalle.postRangoFechas),

    #actualizar un horariodetalle PUT/DELETE
    url(r'^duenio/horariodetalle/(?P<pk>[0-9]+)/(?P<tk>[0-9a-zA-Z]+)/$', vistaHorariodetalle.detalle_objetos),# Obtiene uno en especifico
    url(r'^duenio/(?P<pk>[0-9]+)/horariosdetalle/(?P<tk>[0-9a-zA-Z]+)/$', vistaHorariodetalle.lista_por_duenio),# Otiene el listado de horarios de un duenio

    url(r'^ruta/(?P<tk>[0-9a-zA-Z]+)/$', vistaRuta.lista_objetos),
    url(r'^ruta/(?P<pk>[0-9]+)/(?P<tk>[0-9a-zA-Z]+)/$', vistaRuta.detalle_objetos),
    url(r'^duenio/bus/(?P<pk>[0-9]+)/editar/(?P<tk>[0-9a-zA-Z]+)/$', vistaBus.detalle_objetos),
    url(r'^recurso/(?P<tk>[0-9a-zA-Z]+)/$', vistaRecurso.lista_objetos),
    url(r'^recurso/(?P<pk>[0-9]+)/(?P<tk>[0-9a-zA-Z]+)/$', vistaRecurso.detalle_objetos),

    #url denuncia para movil
    url(r'^denuncia/$', vistaDenuncia.lista_objetos,{'var': 0}),
    url(r'^denuncia/recursos$', vistaDenuncia.lista_objetos,{'var': 1}),
    url(r'^denuncia/recurso$', vistaRecurso.lista_objetos),
    url(r'^denuncia/detalle/$', vistaDenuncia.detalle_objetos,{'var': 0}),
    url(r'^denuncia/detalle/recursos/$', vistaDenuncia.detalle_objetos,{'var': 1}),
    url(r'^denuncia/tipo/$', vistaTipodenuncia.lista_objetos),
    url(r'^denuncia/tipo/(?P<pk>[0-9]+)$', vistaTipodenuncia.detalle_objetos),

    url(r'^operador/denuncias/ruta/(?P<pk>[0-9]+)$', vistaDenuncia.detalle_objetos),
    url(r'^tipodenuncia/$', vistaTipodenuncia.lista_objetos),

    #horariodetalle
    url(r'^horariosdetalle/piloto/(?P<pk>[0-9]+)/(?P<tk>[0-9a-zA-Z]+)/$', vistaHorariodetalle.detalle_Choferes),

    #url modulo PMT
    url(r'^pmt/duenio/(?P<tk>[0-9a-zA-Z]+)/$', vistaDuenio.lista_objetos),
    url(r'^pmt/duenio/(?P<pk>[0-9]+)/(?P<tk>[0-9a-zA-Z]+)/$', vistaDuenio.detalle_objetos),
    url(r'^pmt/ruta/(?P<tk>[0-9a-zA-Z]+)/$', vistaRuta.lista_objetos),
    url(r'^pmt/rutas/(?P<tk>[0-9a-zA-Z]+)/$', vistaRuta.lista_objetos),
    url(r'^pmt/ruta/(?P<pk>[0-9]+)/(?P<tk>[0-9a-zA-Z]+)/$', vistaRuta.detalle_objetos),
    url(r'^pmt/horario/(?P<tk>[0-9a-zA-Z]+)/$', vistaHorario.lista_objetos),
    url(r'^pmt/denuncias/pilotos/(?P<tk>[0-9a-zA-Z]+)/$', vistaChofer.lista_choferes_denuncias),
    url(r'^pmt/horariosdetalle/(?P<tk>[0-9a-zA-Z]+)/$', vistaDuenio.lista_horariodetalle),

    #endPoints sesion
    url(r'^sesion/$', vistaUsuario.crear_usuario),
    url(r'^sesion/log/$', vistaUsuario.autenticar),
    url(r'^sesion/(?P<pk>[0-9]+)/$', vistaUsuario.detalle_usuario),

    #operador
    #estos dendponts por algun motivo no aparecen !
    url(r'^piloto/(?P<pk>[0-9]+)/(?P<tk>[0-9a-zA-Z]+)/$', vistaChofer.chofer_dpi),
    url(r'^bus/(?P<pk>[1-9a-zA-Z]+)/(?P<tk>[0-9a-zA-Z]+)/$', vistaBus.bus_placa),
    url(r'^horariosdetalle/bus/(?P<pk>[1-9]+)/(?P<tk>[0-9a-zA-Z]+)/$', vistaHorariodetalle.lista_por_bus),
    url(r'^denuncias/(?P<tk>[0-9a-zA-Z]+)/$', vistaDenuncia.lista_denuncias),
    url(r'^denuncias/rutas/(?P<tk>[0-9a-zA-Z]+)/$', vistaRuta.lista_numDenuncias),
    url(r'^denuncia/estado/(?P<pk>[0-9]+)/(?P<tk>[0-9a-zA-Z]+)/$', vistaDenuncia.cambio_estado),
    url(r'^denuncias/ruta/(?P<pk>[0-9]+)/(?P<tk>[0-9a-zA-Z]+)/$', vistaRuta.denuncias_ruta),
    url(r'^denuncias/ruta/bus/(?P<idB>[0-9]+)/(?P<tk>[0-9a-zA-Z]+)/$', vistaBus.denuncias_tipodenuncia),
    url(r'^denuncias/ruta/bus/(?P<idB>[0-9]+)/(?P<idTd>[0-9]+)/(?P<tk>[0-9a-zA-Z]+)/$', vistaBus.denuncias_bus_tipodenuncia),


    #Administrador
    url(r'^groups/(?P<tk>[0-9a-zA-Z]+)/$', vistaGrupo.Grupo_Usuario),
    url(r'^groups/(?P<pk>[0-9]+)/(?P<tk>[0-9a-zA-Z]+)/$', vistaGrupo.detalle_objetos),
    url(r'^users/crearusuario/(?P<tk>[0-9a-zA-Z]+)/$', vistaUsuario.crear_usuario),
    url(r'^users/(?P<tk>[0-9a-zA-Z]+)/$', vistaUsuario.lista_usuario),
    url(r'^users/(?P<pk>[0-9]+)/(?P<tk>[0-9a-zA-Z]+)$', vistaUsuario.detalle_usuario),
    url(r'^users/group/(?P<pk>[0-9]+)/(?P<tk>[0-9a-zA-Z]+)/$', vistaUsuario.Usuarios_Group),
    url(r'^users/habilitar/(?P<pk>[0-9]+)/(?P<tk>[0-9a-zA-Z]+)/$', vistaUsuario.CambiarEstado,{'var': 0}),
    url(r'^users/deshabilitar/(?P<pk>[0-9]+)/(?P<tk>[0-9a-zA-Z]+)/$', vistaUsuario.CambiarEstado,{'var': 1}),
    url(r'^users/cambiargrupo/(?P<pk>[0-9]+)/(?P<tk>[0-9a-zA-Z]+)/$', vistaUsuario.cambiarGrupo),
    url(r'^pmt/sinusuario/(?P<tk>[0-9a-zA-Z]+)/$', vistaPmt.obtener_sinUser),
    url(r'^duenio/sinusuario/(?P<tk>[0-9a-zA-Z]+)/$', vistaDuenio.obtener_sinUser),
    url(r'^cultura/sinusuario/(?P<tk>[0-9a-zA-Z]+)/$', vistaCultura.obtener_sinUser),
    url(r'^pmt/(?P<pk>[0-9]+)/(?P<tk>[0-9a-zA-Z]+)/$', vistaPmt.detalle_objetos),
    url(r'^pmt/(?P<tk>[0-9a-zA-Z]+)/$', vistaPmt.lista_objetos),
    url(r'^cultura/(?P<pk>[0-9]+)/(?P<tk>[0-9a-zA-Z]+)/$', vistaCultura.detalle_objetos),
    url(r'^cultura/(?P<tk>[0-9a-zA-Z]+)/$', vistaCultura.lista_objetos),

    #cultura
    url(r'^cultura/actividad/(?P<tk>[0-9a-zA-Z]+)/$', vistaActividad.lista_objetos),
    url(r'^cultura/actividad/(?P<pk>[0-9]+)/(?P<tk>[0-9a-zA-Z]+)/$', vistaActividad.detalle_objetos),
    url(r'^cultura/actividad/(?P<busq>([2][0][1-9]{2}-([1-9]|[1][0-2])-([0][1-9]|[1-2][0-9]|[3][0-1]))|[1-9a-z\s]+[0-9a-z\s]*)/(?P<tk>[0-9a-zA-Z]+)/$', vistaActividad.busqueda),
    url(r'^cultura/consejos/(?P<tk>[0-9a-zA-Z]+)/$', vistaFechaConsejo.lista_objetos),
    url(r'^cultura/consejo/(?P<tk>[0-9a-zA-Z]+)/$', vistaFechaConsejo.lista_objetos),
    url(r'^cultura/consejos/(?P<pk>[0-9]+)/(?P<tk>[0-9a-zA-Z]+)/$', vistaFechaConsejo.detalle_objetos),
    url(r'^cultura/consejodeldia/(?P<tk>[0-9a-zA-Z]+)/$', vistaConsejo.lista_objetos),
    url(r'^cultura/capitulo/(?P<tk>[0-9a-zA-Z]+)/$', vistaCapitulo.lista_objetos),
    url(r'^cultura/pregunta/(?P<tk>[0-9a-zA-Z]+)/$',vistaPregunta.lista_objetos),
    url(r'^cultura/pregunta/(?P<pk>[0-9]+)/(?P<tk>[0-9a-zA-Z]+)/$',vistaPregunta.detalle_objetos),
    url(r'^cultura/titulo/(?P<tk>[0-9a-zA-Z]+)/$',vistaTitulo.lista_objetos),
    url(r'^cultura/titulo/(?P<pk>[0-9]+)/(?P<tk>[0-9a-zA-Z]+)/$', vistaTitulo.detalle_objetos),
    url(r'^cultura/articulo/(?P<tk>[0-9a-zA-Z]+)/$', vistaArticulo.lista_objetos),
    url(r'^cultura/articulo/(?P<pk>[0-9]+)/(?P<tk>[0-9a-zA-Z]+)/$', vistaArticulo.detalle_objetos),

    #para realizar reportes por duenios
    url(r'^reporte/pmt/RepDuenioBusD/(?P<tk>[0-9a-zA-Z]+)/$', vistaEstadistica.lista_objetos),
    url(r'^reporte/pmt/RepBusRuta/(?P<tk>[0-9a-zA-Z]+)/$', vistaEstadistica.lista_objetos_rutaBus),
    url(r'^reporte/pmt/RepPilotoDen/(?P<tk>[0-9a-zA-Z]+)/$', vistaEstadistica.lista_objetos_pilotoDenuncia),
    url(r'^reporte/pmt/RepDuenioBuses/(?P<tk>[0-9a-zA-Z]+)/$', vistaEstadistica.lista_objetos_duenioBuses),

    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
