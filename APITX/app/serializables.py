from django.contrib.auth.models import User, Group,GroupManager,PermissionsMixin
from app import models
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('__all__')

class PermisionS(serializers.ModelSerializer):
    class Meta:
        model = PermissionsMixin
        fields = ('__all__')

class TxcActividadS(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = models.TxcActividad

class TxcArticuloS(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = models.TxcArticulo

class TxcCapituloS(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = models.TxcCapitulo

class ArticuloCapituloS(serializers.ModelSerializer):
    cap = TxcArticuloS(many=True, read_only=True, source='txcarticulo_set')
    class Meta:
        model = models.TxcCapitulo
        fields = ('numero','titulo','cap')

class TxcPreguntaarticuloS(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = models.TxcPreguntaarticulo

class TxcTituloS(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = models.TxcTitulo

class TxcPreguntaS(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = models.TxcPregunta

class TxdTokenS(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = models.TxdToken

class TxdBusS(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = models.TxdBus

class  TxdChoferS(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = models.TxdChofer

class TxdDenunciaS(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = models.TxdDenuncia

class ChoferesDenuncias(serializers.ModelSerializer):
    denuncias = TxdDenunciaS(many=True, read_only=True, source='txddenuncia_set')
    class Meta:
        model = models.TxdChofer
        fields = ('','denuncias')

class DenunciaChofer(serializers.ModelSerializer):
    choferes = TxdChoferS(many=True, read_only=True, source='txdchofer_set')
    class Meta:
        model = models.TxdDenuncia
        fields = ('iddenuncia','choferes')

class TxdHorariodetalleS(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = models.TxdHorariodetalle


class TxdDuenioS(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = models.TxdDuenio

class TxdPmtS(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = models.TxdPmt

class TxcCulturaS(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = models.TxcCultura

class DueniosChoferBuses(serializers.ModelSerializer):
    choferes = TxdChoferS(many=True, read_only=True, source='txdchofer_set')
    buses = TxdBusS(many=True, read_only=True, source='txdbus_set')
    class Meta:
        model = models.TxdDuenio
        fields = ('idduenio','nombre','apellidos','direccion','empresa','fecha_nac','fecha_crea','dpi','telefono','correo','foto','estado','choferes','buses')

class TxdRutaS(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = models.TxdRuta

class BusesRutas(serializers.ModelSerializer):
    rutas = TxdRutaS(many=True, read_only=True, source='txdruta_set')
    class Meta:
        model = models.TxdBus
        field = ('rutas')

class DueniosRutas(serializers.ModelSerializer):
    rutas = BusesRutas(many=True, read_only=True, source='txdbus_set')
    class Meta:
        model = models.TxdDuenio
        fields = ('idduenio','nombre','apellidos','direccion','empresa','fecha_nac','fecha_crea','dpi','telefono','correo','foto','estado','rutas')


class DueniosBuses(serializers.ModelSerializer):
    buses = TxdBusS(many=True, read_only=True, source='txdbus_set')
    class Meta:
        model = models.TxdDuenio
        fields = ('idduenio','nombre','apellidos','direccion','empresa','fecha_nac','fecha_crea','dpi','telefono','correo','foto','estado','buses')

class DueniosChoferes(serializers.ModelSerializer):
    choferes = TxdChoferS(many=True, read_only=True, source='txdchofer_set')
    class Meta:
        model = models.TxdDuenio
        fields = ('idduenio','nombre','apellidos','direccion','empresa','fecha_nac','fecha_crea','dpi','telefono','correo','foto','estado','choferes')

class TxdHorarioS(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = models.TxdHorario

class Duenios_horariodetalle(serializers.ModelSerializer):
    chofer = TxdChoferS(read_only=True)
    choferes = serializers.PrimaryKeyRelatedField(write_only=True, queryset=models.TxdChofer.objects.filter(duenio=1), source='chofer')
    horario = TxdHorarioS(read_only=True)
    horarios = serializers.PrimaryKeyRelatedField(write_only=True, queryset=models.TxdHorario.objects.filter(duenio=1), source='horario')
    bus = TxdBusS(read_only=True)
    buses = serializers.PrimaryKeyRelatedField(write_only=True, queryset=models.TxdBus.objects.filter(duenio=1), source='bus')

    class Meta:
        model = models.TxdHorariodetalle
        fields = ('idhorariodetalle','fecha','estado','horario','horarios','chofer', 'choferes','bus','buses')

class choferHorariDetalle(serializers.ModelSerializer):
    horariosDetalle = TxdHorariodetalleS(many=True, read_only=True, source='txdhorariodetalle_set')
    class Meta:
        model = models.TxdChofer
        fields = ('idchofer','nombre','apellidos','direccion','dpi','telefono','correo','foto','licencia','tipolicencia','estado','duenio','horariosDetalle')

class listadoDueniosDetalles(serializers.ModelSerializer):
    horariodetalle = serializers.PrimaryKeyRelatedField(write_only=True, queryset=models.TxdHorariodetalle.objects.filter(idhorariodetalle =1), source='duenio')
    class Meta:
        model = models.TxdDuenio
        fields = ('idduenio','nombre','apellidos','direccion','empresa','fecha_nac','fecha_crea','dpi','telefono','correo','foto','estado','horariodetalle')

class DueniosHorarios(serializers.ModelSerializer):
    horarios = TxdHorarioS(many=True, read_only=True, source='txdhorario_set')
    class Meta:
        model = models.TxdDuenio
        fields = ('idduenio','idduenio','nombre','apellidos','direccion','empresa','fecha_nac','fecha_crea','dpi','telefono','correo','foto','estado','horarios')

class TxdRecursoS(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = models.TxdRecurso

class TxdTipodenunciaS(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = models.TxdTipodenuncia
class TxdDenunciaRecursosS(serializers.ModelSerializer):
    recursos = TxdRecursoS(many=True, read_only=True, source='txdrecurso_set')
    class Meta:
        model = models.TxdDenuncia
        fields = ('iddenuncia','recursos')

class TxdDenunciaTipoS(serializers.ModelSerializer):
    denunciaRecurso = TxdDenunciaRecursosS(many=True, read_only=True, source='txddenuncia_set')
    class Meta:
        model = models.TxdTipodenuncia
        fields = ('idtipodenuncia','denunciaRecurso')

class TxcoConsejoS(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = models.TxcoConsejo
class TxcoFechaS(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = models.TxcoFecha
class TxcoConsejosFechaS(serializers.ModelSerializer):
    consejos = TxcoConsejoS(many=True,read_only=True,source='TxcoConsejo_set')
    class Meta:
        model = models.TxcoFecha
        fields = ('idfecha','fecha','consejos','consejo')

class TxcoCapituloTituloS(serializers.ModelSerializer):
    capitulos = TxcCapituloS(many=True, read_only=True, source='txccapitulo_set')
    class Meta:
        model = models.TxcTitulo
        fields = ('idtitulo','titulo','numero','capitulos')

class BusRutaS(serializers.ModelSerializer):
    bs = TxdBusS(many=True, read_only=True, source='txdbus_set')
    class Meta:
        model = models.TxdRuta
        fields = ('idruta','nombre','recorrido','bs')

class ChoferDenunciaS(serializers.ModelSerializer):
    den = TxdDenunciaS(many=True, read_only=True, source='txddenuncia_set')
    class Meta:
        model = models.TxdChofer
        fields = ('idchofer','nombre','dpi','den')
