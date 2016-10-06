# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models

class TxcActividad(models.Model):
    idactividad = models.AutoField(db_column='idActividad', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.TextField()
    fecha = models.DateTimeField()
    lugar = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=250, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'txc_actividad'


class TxcTitulo(models.Model):
    idtitulo = models.AutoField(db_column='idTitulo', primary_key=True)  # Field name made lowercase.
    titulo = models.CharField(max_length=100, blank=True, null=True)
    numero = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'txc_titulo'


class TxcCapitulo(models.Model):
    idcapitulo = models.AutoField(db_column='idCapitulo', primary_key=True)  # Field name made lowercase.
    titulo = models.CharField(max_length=100, blank=True, null=True)
    numero = models.IntegerField(blank=True, null=True)
    titulo_0 = models.ForeignKey(TxcTitulo, models.DO_NOTHING, db_column='Titulo_id')  # Field name made lowercase. Field renamed because of name conflict.

    class Meta:
        db_table = 'txc_capitulo'


class TxcArticulo(models.Model):
    idarticulo = models.AutoField(db_column='idArticulo', primary_key=True)  # Field name made lowercase.
    descripcion = models.TextField()
    numero = models.IntegerField(blank=True, null=True)
    titulo = models.CharField(max_length=100, blank=True, null=True)
    capitulo = models.ForeignKey(TxcCapitulo, models.DO_NOTHING, db_column='Capitulo_id')  # Field name made lowercase.

    class Meta:
        db_table = 'txc_articulo'


class TxcPregunta(models.Model):
    idpregunta = models.AutoField(db_column='idPregunta', primary_key=True)  # Field name made lowercase.
    pregunta = models.TextField(blank=True, null=True)
    respuesta = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'txc_pregunta'


class TxcPreguntaarticulo(models.Model):
    idpreguntaarticulo = models.AutoField(db_column='idPreguntaArticulo', primary_key=True)  # Field name made lowercase.
    pregunta = models.ForeignKey(TxcPregunta, models.DO_NOTHING, db_column='Pregunta_id')  # Field name made lowercase.
    articulo = models.ForeignKey(TxcArticulo, models.DO_NOTHING, db_column='Articulo_id')  # Field name made lowercase.

    class Meta:
        db_table = 'txc_preguntaarticulo'


class TxcoConsejo(models.Model):
    idconsejo = models.AutoField(db_column='idConsejo', primary_key=True)  # Field name made lowercase.
    consejo = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'txco_consejo'


class TxcoFecha(models.Model):
    idfecha = models.AutoField(db_column='idFecha', primary_key=True)  # Field name made lowercase.
    fecha = models.DateField(blank=True, null=True)
    consejo = models.ForeignKey(TxcoConsejo, models.DO_NOTHING, db_column='Consejo_id')  # Field name made lowercase.

    class Meta:
        db_table = 'txco_fecha'


class TxdDuenio(models.Model):
    idduenio = models.AutoField(db_column='idDuenio', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=45)
    apellidos = models.CharField(max_length=45)
    direccion = models.CharField(max_length=45)
    dpi = models.IntegerField()
    telefono = models.IntegerField(blank=True, null=True)
    correo = models.CharField(max_length=45, blank=True, null=True)
    foto = models.CharField(max_length=100)
    estado = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'txd_duenio'


class TxdRuta(models.Model):
    idruta = models.AutoField(db_column='idRuta', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=45, blank=True, null=True)
    recorrido = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'txd_ruta'


class TxdBus(models.Model):
    idbus = models.AutoField(db_column='idBus', primary_key=True)  # Field name made lowercase.
    placa = models.CharField(max_length=8)
    color = models.CharField(max_length=20)
    modelo = models.CharField(max_length=45, blank=True, null=True)
    marca = models.CharField(max_length=20)
    numbus = models.IntegerField()
    observaciones = models.TextField(blank=True, null=True)
    foto = models.CharField(max_length=100, blank=True, null=True)
    duenio = models.ForeignKey(TxdDuenio, models.DO_NOTHING, db_column='Duenio_id')  # Field name made lowercase.
    ruta = models.ForeignKey(TxdRuta, models.DO_NOTHING, db_column='Ruta_id')  # Field name made lowercase.
    estado = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'txd_bus'


class TxdChofer(models.Model):
    idchofer = models.AutoField(db_column='idChofer', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=45)
    apellidos = models.CharField(max_length=45)
    direccion = models.CharField(max_length=45, blank=True, null=True)
    dpi = models.IntegerField()
    telefono = models.IntegerField(blank=True, null=True)
    correo = models.CharField(max_length=45, blank=True, null=True)
    foto = models.CharField(max_length=100, blank=True, null=True)
    licencia = models.CharField(max_length=1)
    tipolicencia = models.CharField(db_column='tipoLicencia', max_length=2, blank=True, null=True)  # Field name made lowercase.
    nolicencia = models.IntegerField(db_column='noLicencia', blank=True, null=True)  # Field name made lowercase.
    estado = models.IntegerField(blank=True, null=True)
    duenio = models.ForeignKey(TxdDuenio, models.DO_NOTHING, db_column='Duenio_id')  # Field name made lowercase.

    class Meta:
        db_table = 'txd_chofer'


class TxdTipodenuncia(models.Model):
    idtipodenuncia = models.AutoField(db_column='idTipodenuncia', primary_key=True)  # Field name made lowercase.
    descripcion = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'txd_tipodenuncia'


class TxdDenuncia(models.Model):
    iddenuncia = models.BigAutoField(db_column='idDenuncia', primary_key=True)  # Field name made lowercase.
    idhash = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.IntegerField(blank=True, null=True)
    fechahora = models.DateTimeField(blank=True, null=True)
    tipodenuncia = models.ForeignKey(TxdTipodenuncia, models.DO_NOTHING, db_column='Tipodenuncia_id')  # Field name made lowercase.
    placa = models.CharField(max_length=7, blank=True, null=True)
    chofer = models.ForeignKey(TxdChofer, models.DO_NOTHING, db_column='Chofer_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'txd_denuncia'

class TxdHorario(models.Model):
    idhorario = models.AutoField(db_column='idHorario', primary_key=True)  # Field name made lowercase.
    horainicio = models.TimeField()
    horafin = models.TimeField()
    duenio = models.ForeignKey(TxdDuenio, models.DO_NOTHING, db_column='Duenio_id')  # Field name made lowercase.

    class Meta:
        db_table = 'txd_horario'


class TxdHorariodetalle(models.Model):
    idhorariodetalle = models.AutoField(db_column='idHorarioDetalle', primary_key=True)  # Field name made lowercase.
    bus = models.ForeignKey(TxdBus, models.DO_NOTHING, db_column='Bus_id')  # Field name made lowercase.
    chofer = models.ForeignKey(TxdChofer, models.DO_NOTHING, db_column='Chofer_id')  # Field name made lowercase.
    horario = models.ForeignKey(TxdHorario, models.DO_NOTHING, db_column='Horario_id')  # Field name made lowercase.
    fecha = models.DateField()

    class Meta:
        db_table = 'txd_horariodetalle'


class TxdRecurso(models.Model):
    idrecurso = models.AutoField(db_column='idRecurso', primary_key=True)  # Field name made lowercase.
    direccion = models.CharField(max_length=100, blank=True, null=True)
    denuncia = models.ForeignKey(TxdDenuncia, models.DO_NOTHING, db_column='Denuncia_id')  # Field name made lowercase.

    class Meta:
        db_table = 'txd_recurso'


class TxuRol(models.Model):
    idrol = models.AutoField(db_column='idRol', primary_key=True)  # Field name made lowercase.
    rol = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'txu_rol'


class TxuUsuario(models.Model):
    idpersona = models.AutoField(db_column='idPersona', primary_key=True)  # Field name made lowercase.
    nombre = models.IntegerField(blank=True, null=True)
    direccion = models.CharField(max_length=45, blank=True, null=True)
    telefono = models.CharField(max_length=8, blank=True, null=True)
    correo = models.CharField(max_length=45, blank=True, null=True)
    dpi = models.CharField(max_length=13, blank=True, null=True)
    estado = models.IntegerField(blank=True, null=True)
    usuario = models.CharField(max_length=45, blank=True, null=True)
    contrasenia = models.CharField(max_length=45, blank=True, null=True)
    rol = models.ForeignKey(TxuRol, models.DO_NOTHING, db_column='Rol_id')  # Field name made lowercase.

    class Meta:
        db_table = 'txu_usuario'
