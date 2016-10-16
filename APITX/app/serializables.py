from django.contrib.auth.models import User, Group
from app import models
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class TxcActividadS(serializers.ModelSerializer):
    class Meta:
        model = models.TxcActividad

class TxcArticuloS(serializers.ModelSerializer):
    class Meta:
        model = models.TxcArticulo

class TxcCapituloS(serializers.ModelSerializer):
    class Meta:
        model = models.TxcCapitulo

class TxcPreguntaarticuloS(serializers.ModelSerializer):
    class Meta:
        model = models.TxcPreguntaarticulo

class TxcTituloS(serializers.ModelSerializer):
    class Meta:
        model = models.TxcTitulo

class TxcPreguntaS(serializers.ModelSerializer):
    class Meta:
        model = models.TxcPregunta

class TxdTokenS(serializers.ModelSerializer):
    class Meta:
        model = models.TxdToken

class TxdBusS(serializers.ModelSerializer):
    class Meta:
        model = models.TxdBus

class  TxdChoferS(serializers.ModelSerializer):
    class Meta:
        model = models.TxdChofer

class TxdDenunciaS(serializers.ModelSerializer):
    class Meta:
        model = models.TxdDenuncia

class ChoferesDenuncias(serializers.ModelSerializer):
    denuncias = TxdDenunciaS(many=True, read_only=True, source='txddenuncia_set')
    class Meta:
        model = models.TxdChofer
        fields = ('','denuncias')

class TxdHorariodetalleS(serializers.ModelSerializer):
    class Meta:
        model = models.TxdHorariodetalle


class TxdDuenioS(serializers.ModelSerializer):
    class Meta:
        model = models.TxdDuenio
class DueniosChoferBuses(serializers.ModelSerializer):
    choferes = TxdChoferS(many=True, read_only=True, source='txdchofer_set')
    buses = TxdBusS(many=True, read_only=True, source='txdbus_set')
    class Meta:
        model = models.TxdDuenio
        fields = ('idduenio','nombre','apellidos','direccion','dpi','telefono','correo','foto','estado','choferes','buses')

class TxdRutaS(serializers.ModelSerializer):
    class Meta:
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
        fields = ('idduenio','nombre','apellidos','direccion','dpi','telefono','correo','foto','estado','rutas')


class DueniosBuses(serializers.ModelSerializer):
    buses = TxdBusS(many=True, read_only=True, source='txdbus_set')
    class Meta:
        model = models.TxdDuenio
        fields = ('idduenio','nombre','apellidos','direccion','dpi','telefono','correo','foto','estado','buses')

class DueniosChoferes(serializers.ModelSerializer):
    choferes = TxdChoferS(many=True, read_only=True, source='txdchofer_set')
    class Meta:
        model = models.TxdDuenio
        fields = ('idduenio','nombre','apellidos','direccion','dpi','telefono','correo','foto','estado','choferes')

class TxdHorarioS(serializers.ModelSerializer):
    class Meta:
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
        fields = ('idhorariodetalle','fecha','horario','horarios','chofer', 'choferes','bus','buses')

class DueniosHorarios(serializers.ModelSerializer):
    horarios = TxdHorarioS(many=True, read_only=True, source='txdhorario_set')
    class Meta:
        model = models.TxdDuenio
        fields = ('idduenio','idduenio','nombre','apellidos','direccion','dpi','telefono','correo','foto','estado','horarios')

class TxdRecursoS(serializers.ModelSerializer):
    class Meta:
        model = models.TxdRecurso

class TxdTipodenunciaS(serializers.ModelSerializer):
    class Meta:
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
        model = models.TxcoConsejo
class TxcoFechaS(serializers.ModelSerializer):
    class Meta:
        model = models.TxcoFecha
class ConsejosFecha(serializers.ModelSerializer):
    fechas=TxcoFechaS(many=True, read_only=True,source='TxcoFecha_set')
    class Meta:
        model = models.TxcoConsejo
        fields = ('idconsejo','fechas')
