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
                        vistaArticulo, autenticacion, vistaUsuario, vistaPmt,vistaGrupo,vistaCultura,vistaEstadistica,vistadenunciaWeb)
from APITX import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
#router.register(r'users', vistaGrupoUsuario.UserViewSet)
#router.register(r'groups', vistaGrupoUsuario.GroupViewSet)

urlpatterns = [

    url(r'^obtenertoken/', autenticacion.token),
    url(r'^admin/', admin.site.urls),
    url(r'^duenio/$', vistaDuenio.lista_objetos),
    url(r'^operador/duenios/$', vistaDuenio.lista_objetos),
    url(r'^admin/duenio/lista/$', vistaDuenio.lista_objetos),
    url(r'user/$', vistaGrupoUsuario.UserViewSet),

    url(r'^duenio/(?P<pk>[0-9]+)/$', vistaDuenio.detalle_objetos),
    url(r'^duenio/(?P<pk>[0-9]+)/principal/$', vistaDuenio.principal_duenio_choferes,{'var': 0}),
    url(r'^duenio/(?P<pk>[0-9]+)/pilotos/$', vistaDuenio.principal_duenio_choferes,{'var': 1}),
    url(r'^duenio/(?P<pk>[0-9]+)/buses/$', vistaDuenio.principal_duenio_choferes,{'var': 3}),
    url(r'^duenio/(?P<pk>[0-9]+)/completo/$', vistaDuenio.principal_duenio_choferes,{'var': 4}),
    url(r'^duenio/(?P<pk>[0-9]+)/rutas-buses/$', vistaDuenio.principal_duenio_choferes,{'var': 5}),
    url(r'^duenio/piloto/$', vistaChofer.lista_objetos),
    url(r'^duenio/piloto/(?P<pk>[0-9]+)/$', vistaChofer.detalle_objetos),
    url(r'^duenio/piloto/(?P<pk>[0-9]+)/editar//$', vistaChofer.detalle_objetos),
    url(r'^duenio/bus/$', vistaBus.lista_objetos),
    url(r'^duenio/bus/(?P<pk>[0-9]+)/$', vistaBus.detalle_objetos),
    url(r'^duenio/horario/$', vistaHorario.lista_objetos),
    url(r'^duenio/horario/(?P<pk>[0-9]+)/$', vistaHorario.detalle_objetos),
    url(r'^duenio/(?P<pk>[0-9]+)/horarios/$', vistaHorario.horarios_duenio),
    url(r'^duenio/horariodetalle/$', vistaHorariodetalle.lista_objetos),
    url(r'^duenio/horariosdetalle/$', vistaHorariodetalle.lista_objetos), # obtiene todos los horarios y detalles
    url(r'^duenio/horariodetalle/(?P<fInicio>20[0-9][0-9]-[0-1][0-9]-[0-3][0-9])/(?P<fFin>20[0-9][0-9]-[0-1][0-9]-[0-3][0-9])/$', vistaHorariodetalle.rango),
    url(r'^duenio/horariosdetalle/crearrango/$',vistaHorariodetalle.postRangoFechas),
    url(r'^duenio/todainformacion/$',vistaDuenio.todaInformacion),

    #actualizar un horariodetalle PUT/DELETE
    url(r'^duenio/horariodetalle/(?P<pk>[0-9]+)/$', vistaHorariodetalle.detalle_objetos),# Obtiene uno en especifico
    url(r'^duenio/(?P<pk>[0-9]+)/horariosdetalle/$', vistaHorariodetalle.lista_por_duenio),# Otiene el listado de horarios de un duenio
    url(r'^ruta/$', vistaRuta.lista_objetos),
    url(r'^ruta/(?P<pk>[0-9]+)/$', vistaRuta.detalle_objetos),
    url(r'^duenio/bus/(?P<pk>[0-9]+)/editar/$', vistaBus.detalle_objetos),
    url(r'^recurso/$', vistaRecurso.lista_objetos),
    url(r'^recurso/(?P<pk>[0-9]+)/$', vistaRecurso.detalle_objetos),

    #url denuncia para movil
    url(r'^denuncia/$', vistaDenuncia.lista_objetos,{'var': 0}),
    url(r'^denuncia/recursos$', vistaDenuncia.lista_objetos,{'var': 1}),
    url(r'^denuncia/recurso$', vistaRecurso.lista_objetos),
    url(r'^denuncia/detalle/$', vistaDenuncia.detalle_objetos,{'var': 0}),
    url(r'^denuncia/detalle/recursos/$', vistaDenuncia.detalle_objetos,{'var': 1}),
    url(r'^denuncia/tipo/$', vistaTipodenuncia.lista_objetos),
    url(r'^denuncia/tipo/(?P<pk>[0-9]+)/$', vistaTipodenuncia.detalle_objetos),

    url(r'^operador/denuncias/ruta/(?P<pk>[0-9]+)$', vistaDenuncia.detalle_objetos),
    url(r'^tipodenuncia/$', vistaTipodenuncia.lista_objetos),

    #horariodetalle
    url(r'^horariosdetalle/piloto/(?P<pk>[0-9]+)/$', vistaHorariodetalle.detalle_Choferes),

    #url modulo PMT
    url(r'^pmt/duenio/$', vistaDuenio.lista_objetos),
    url(r'^pmt/duenio/(?P<pk>[0-9]+)/$', vistaDuenio.detalle_objetos),
    url(r'^pmt/ruta/$', vistaRuta.lista_objetos),
    url(r'^pmt/rutas/$', vistaRuta.lista_objetos),
    url(r'^pmt/ruta/(?P<pk>[0-9]+)/$', vistaRuta.detalle_objetos),
    url(r'^pmt/horario/$', vistaHorario.lista_objetos),
    url(r'^pmt/denuncias/pilotos/$', vistaChofer.lista_choferes_denuncias),
    url(r'^pmt/horariosdetalle/$', vistaDuenio.lista_horariodetalle),

    #endPoints sesion
    url(r'^sesion/$', vistaUsuario.crear_usuario),
    url(r'^sesion/(?P<pk>[0-9]+)/$', vistaUsuario.detalle_usuario),

    #operador
    #estos dendponts por algun motivo no aparecen !
    url(r'^piloto/(?P<pk>[0-9]+)/$', vistaChofer.chofer_dpi),
    url(r'^bus/(?P<pk>[1-9a-zA-Z]+)/$', vistaBus.bus_placa),
    url(r'^horariosdetalle/bus/(?P<pk>[1-9]+)/$', vistaHorariodetalle.lista_por_bus),
    url(r'^webdenuncias/$', vistaDenuncia.lista_denuncias),
    url(r'^webdenuncias/rango/$', vistaDenuncia.lista_denuncias_rango),
    url(r'^denuncias/rutas/$', vistaRuta.lista_numDenuncias),
    url(r'^denuncia/estado/(?P<pk>[0-9]+)/$', vistaDenuncia.cambio_estado),
    url(r'^denuncias/cambiarestados/$', vistaDenuncia.cambio_estados),
    url(r'^denuncias/ruta/(?P<pk>[0-9]+)/$', vistaRuta.denuncias_ruta),
    url(r'^denuncias/ruta/bus/(?P<idB>[0-9]+)/$', vistaBus.denuncias_tipodenuncia),
    url(r'^denuncias/ruta/bus/(?P<idB>[0-9]+)/(?P<idTd>[0-9]+)/$', vistaBus.denuncias_bus_tipodenuncia),
    url(r'^denuncias/tiposestados/$', vistaDenuncia.estados),


    #Administrador
    url(r'^groups/$', vistaGrupo.Grupo_Usuario),
    url(r'^groups/(?P<pk>[0-9]+)/$', vistaGrupo.detalle_objetos),
    url(r'^users/crearusuario/$', vistaUsuario.crear_usuario),
    url(r'^users/$', vistaUsuario.lista_usuario),
    url(r'^users/cambiarcontrasenia/(?P<pk>[0-9]+)/$', vistaUsuario.cambiarContrasenia),
    url(r'^users/cambiarcontreniausuario/(?P<pk>[0-9]+)/$', vistaUsuario.cambiarContreniaUsuario),
    url(r'^users/(?P<pk>[0-9]+)/$', vistaUsuario.detalle_usuario),
    url(r'^users/group/(?P<pk>[0-9]+)/$', vistaUsuario.Usuarios_Group),
    url(r'^users/habilitar/(?P<pk>[0-9]+)/$', vistaUsuario.CambiarEstado,{'var': 0}),
    url(r'^users/deshabilitar/(?P<pk>[0-9]+)/$', vistaUsuario.CambiarEstado,{'var': 1}),
    url(r'^users/cambiargrupo/(?P<pk>[0-9]+)/$', vistaUsuario.cambiarGrupo),
    url(r'^pmt/sinusuario/$', vistaPmt.obtener_sinUser),
    url(r'^duenio/sinusuario/$', vistaDuenio.obtener_sinUser),
    url(r'^cultura/sinusuario/$', vistaCultura.obtener_sinUser),
    url(r'^pmt/(?P<pk>[0-9]+)/$', vistaPmt.detalle_objetos),
    url(r'^pmt/$', vistaPmt.lista_objetos),
    url(r'^cultura/(?P<pk>[0-9]+)/$', vistaCultura.detalle_objetos),
    url(r'^cultura/$', vistaCultura.lista_objetos),

    #cultura
    url(r'^cultura/actividad/$', vistaActividad.lista_objetos),
    url(r'^cultura/actividad/(?P<pk>[0-9]+)/$', vistaActividad.detalle_objetos),
    url(r'^cultura/actividad/(?P<busq>([2][0][1-9]{2}-([1-9]|[1][0-2])-([0][1-9]|[1-2][0-9]|[3][0-1]))|[1-9a-z\s]+[0-9a-z\s]*)/$', vistaActividad.busqueda),
    url(r'^cultura/consejos/$', vistaFechaConsejo.lista_objetos),
    url(r'^cultura/consejo/$', vistaFechaConsejo.lista_objetos),
    url(r'^cultura/consejos/(?P<pk>[0-9]+)/$', vistaFechaConsejo.detalle_objetos),
    url(r'^cultura/consejodeldia/$', vistaConsejo.lista_objetos),
    url(r'^cultura/capitulo/$', vistaCapitulo.lista_objetos),
    url(r'^cultura/pregunta/$',vistaPregunta.lista_objetos),
    url(r'^cultura/pregunta/(?P<pk>[0-9]+)/$',vistaPregunta.detalle_objetos),
    url(r'^cultura/titulo/$',vistaTitulo.lista_objetos),
    url(r'^cultura/titulo/(?P<pk>[0-9]+)/$', vistaTitulo.detalle_objetos),
    url(r'^cultura/articulo/$', vistaArticulo.lista_objetos),
    url(r'^cultura/articulo/(?P<pk>[0-9]+)/$', vistaArticulo.detalle_objetos),
    url(r'^cultura/consejoAct/$',vistaConsejo.principal_consejoActividad),
    url(r'^cultura/actividades/outtk$',vistaActividad.lista),
    url(r'^cultura/consejofe/$',vistaConsejo.principal_consejofecha),

    #para realizar reportes para pmt
    url(r'^reporte/pmt/RepDuenioBusD/$', vistaEstadistica.lista_objetos),
    url(r'^reporte/pmt/RepBusRuta/$', vistaEstadistica.lista_objetos_rutaBus),
    url(r'^reporte/pmt/RepPilotoDen/$', vistaEstadistica.lista_objetos_pilotoDenuncia),
    url(r'^reporte/pmt/RepDuenioBuses/$', vistaEstadistica.lista_objetos_duenioBuses),
    #generar reportes para duenios
    url(r'^reporte/duenio/RepDuenioBusesId/(?P<pk>[0-9]+)/$', vistaEstadistica.lista_objetos_duenioBusesId),
    url(r'^reporte/duenio/RepDuenioChoferId/(?P<pk>[0-9]+)/$', vistaEstadistica.lista_objetos_duenioChofId),
    url(r'^reporte/duenio/RepBusChofId/(?P<pk>[0-9]+)/$', vistaEstadistica.lista_objetos_busChofId),
    url(r'^reporte/duenio/RepTipoDenD/$', vistaEstadistica.lista_objetos_tipoDenDenuncia),

    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
