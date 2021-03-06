# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class TxcActividad(models.Model):
    idactividad = models.AutoField(db_column='idActividad', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.TextField()
    fecha = models.DateTimeField()
    lugar = models.CharField(max_length=100)
    latitud = models.FloatField(null=True)
    longitud = models.FloatField(null=True)
    direccion = models.TextField(blank=True, null=True)
    estado = models.BooleanField()
    class Meta:
        permissions = (
            ("view_txcactividad", "Can see available actividad"),
        )
        db_table = 'txc_actividad'


class TxcTitulo(models.Model):
    idtitulo = models.AutoField(db_column='idTitulo', primary_key=True)  # Field name made lowercase.
    titulo = models.CharField(max_length=100, blank=True, null=True)
    numero = models.IntegerField(blank=True, null=True)

    class Meta:
        permissions = (
            ("view_txctitulo", "Can see available titulo"),
        )
        db_table = 'txc_titulo'


class TxcCapitulo(models.Model):
    idcapitulo = models.AutoField(db_column='idCapitulo', primary_key=True)  # Field name made lowercase.
    titulo = models.CharField(max_length=100, blank=True, null=True)
    numero = models.IntegerField(blank=True, null=True)
    titulo_0 = models.ForeignKey(TxcTitulo, models.DO_NOTHING, db_column='Titulo_id')  # Field name made lowercase. Field renamed because of name conflict.

    class Meta:
        permissions = (
            ("view_txccapitulo", "Can see available capitulo"),
        )
        db_table = 'txc_capitulo'


class TxcArticulo(models.Model):
    idarticulo = models.AutoField(db_column='idArticulo', primary_key=True)  # Field name made lowercase.
    descripcion = models.TextField()
    numero = models.IntegerField(blank=True, null=True)
    titulo = models.CharField(max_length=100, blank=True, null=True)
    capitulo = models.ForeignKey(TxcCapitulo, models.DO_NOTHING, db_column='Capitulo_id')  # Field name made lowercase.

    class Meta:
        permissions = (
            ("view_txcarticulo", "Can see available articulo"),
        )
        db_table = 'txc_articulo'


class TxcPregunta(models.Model):
    idpregunta = models.AutoField(db_column='idPregunta', primary_key=True)  # Field name made lowercase.
    pregunta = models.TextField(blank=True, null=True)
    respuesta = models.TextField(blank=True, null=True)

    class Meta:
        permissions = (
            ("view_txcpregunta", "Can see available pregunta"),
        )
        db_table = 'txc_pregunta'


class TxcPreguntaarticulo(models.Model):
    idpreguntaarticulo = models.AutoField(db_column='idPreguntaArticulo', primary_key=True)  # Field name made lowercase.
    pregunta = models.ForeignKey(TxcPregunta, models.DO_NOTHING, db_column='Pregunta_id')  # Field name made lowercase.
    articulo = models.ForeignKey(TxcArticulo, models.DO_NOTHING, db_column='Articulo_id')  # Field name made lowercase.

    class Meta:
        permissions = (
            ("view_txcpreguntaarticulo", "Can see available txcpreguntaarticulo"),
        )
        db_table = 'txc_preguntaarticulo'


class TxcoConsejo(models.Model):
    idconsejo = models.AutoField(db_column='idConsejo', primary_key=True)  # Field name made lowercase.
    consejo = models.TextField(blank=True, null=True)

    class Meta:
        permissions = (
            ("view_txcoconsejo", "Can see available consejo"),
        )
        db_table = 'txco_consejo'


class TxcoFecha(models.Model):
    idfecha = models.AutoField(db_column='idFecha', primary_key=True)  # Field name made lowercase.
    fecha = models.DateField(blank=True, null=True)
    consejo = models.ForeignKey(TxcoConsejo, models.DO_NOTHING, db_column='Consejo_id')  # Field name made lowercase.

    class Meta:
        permissions = (
            ("view_txcofecha", "Can see available fecha"),
        )
        db_table = 'txco_fecha'


class TxdDuenio(models.Model):
    idduenio = models.AutoField(db_column='idDuenio', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=45)
    apellidos = models.CharField(max_length=45)
    direccion = models.CharField(max_length=45)
    empresa = models.CharField(max_length=45)
    fecha_nac = models.DateTimeField()
    fecha_crea = models.DateTimeField()
    dpi =models.CharField(max_length=13)
    telefono = models.IntegerField(blank=True, null=True)
    correo = models.CharField(max_length=45, blank=True, null=True)
    foto = models.ImageField(upload_to='duenio/',blank=True, null=True)
    estado = models.IntegerField(blank=True, null=True)
    usuario = models.ForeignKey(User, models.DO_NOTHING, db_column='usuario_id', blank=True, null=True)

    class Meta:
        permissions = (
            ("view_txdduenio", "Can see available duenio"),
        )
        db_table = 'txd_duenio'

class TxcCultura(models.Model):
    idcultura = models.AutoField(db_column='idCultura', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=45)
    apellidos = models.CharField(max_length=45)
    direccion = models.CharField(max_length=45)
    dpi = models.CharField(max_length=13)
    telefono = models.IntegerField(blank=True, null=True)
    correo = models.CharField(max_length=45, blank=True, null=True)
    foto = models.ImageField(upload_to='cultura/',blank=True, null=True)
    estado = models.IntegerField(blank=True, null=True)
    usuario = models.ForeignKey(User, models.DO_NOTHING, db_column='usuario_id', blank=True, null=True)

    class Meta:
        permissions = (
            ("view_txccultura", "Can see available cultura"),
        )
        db_table = 'txc_cultura'

class TxdPmt(models.Model):
    idpmt = models.AutoField(db_column='idPmt', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=45)
    apellidos = models.CharField(max_length=45)
    direccion = models.CharField(max_length=45)
    dpi = models.CharField(max_length=13)
    telefono = models.IntegerField(blank=True, null=True)
    correo = models.CharField(max_length=45, blank=True, null=True)
    foto = models.ImageField(upload_to='pmt/',blank=True, null=True)
    estado = models.IntegerField(blank=True, null=True)
    usuario = models.ForeignKey(User, models.DO_NOTHING, db_column='usuario_id', blank=True, null=True)

    class Meta:
        permissions = (
            ("view_txdpmt", "Can see available pmt"),
        )
        db_table = 'txd_pmt'

class TxdRuta(models.Model):
    idruta = models.AutoField(db_column='idRuta', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=45, blank=True, null=True)
    recorrido = models.TextField(blank=True, null=True)

    class Meta:
        permissions = (
            ("view_txdruta", "Can see available ruta"),
        )
        db_table = 'txd_ruta'

class TxdToken(models.Model):
    idtoken = models.AutoField(db_column='idToken', primary_key=True)  # Field name made lowercase.
    token = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        permissions = (
            ("view_txdtoken", "Can see available Token"),
        )
        db_table = 'txd_Token'

class TxdBus(models.Model):
    idbus = models.AutoField(db_column='idBus', primary_key=True)  # Field name made lowercase.
    placa = models.CharField(max_length=8)
    color = models.CharField(max_length=20)
    modelo = models.CharField(max_length=45, blank=True, null=True)
    marca = models.CharField(max_length=20)
    numbus = models.IntegerField()
    observaciones = models.TextField(blank=True, null=True)
    foto = models.ImageField(upload_to='bus/',blank=True, null=True)
    duenio = models.ForeignKey(TxdDuenio, models.DO_NOTHING, db_column='Duenio_id')  # Field name made lowercase.
    ruta = models.ForeignKey(TxdRuta, models.DO_NOTHING, db_column='Ruta_id')  # Field name made lowercase.
    estado = models.IntegerField(blank=True, null=True)

    class Meta:
        permissions = (
            ("view_txdbus", "Can see available bus"),
        )
        db_table = 'txd_bus'


class TxdChofer(models.Model):
    idchofer = models.AutoField(db_column='idChofer', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=45)
    apellidos = models.CharField(max_length=45)
    direccion = models.CharField(max_length=45, blank=True, null=True)
    dpi = models.CharField(max_length=13, blank=True, null=True)
    telefono = models.IntegerField(blank=True, null=True)
    correo = models.CharField(max_length=45, blank=True, null=True)
    foto =  models.ImageField(upload_to='chofer/',blank=True, null=True)
    licencia = models.CharField(max_length=11)
    tipolicencia = models.CharField(db_column='tipoLicencia', max_length=2, blank=True, null=True)  # Field name made lowercase.
    #nolicencia = models.IntegerField(db_column='noLicencia', blank=True, null=True)  # Field name made lowercase.
    estado = models.IntegerField(blank=True, null=True)
    duenio = models.ForeignKey(TxdDuenio, models.DO_NOTHING, db_column='Duenio_id')  # Field name made lowercase.

    class Meta:
        permissions = (
            ("view_txdchofer", "Can see available chofer"),
        )
        db_table = 'txd_chofer'


class TxdTipodenuncia(models.Model):
    idtipodenuncia = models.AutoField(db_column='idTipodenuncia', primary_key=True)  # Field name made lowercase.
    descripcion = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        permissions = (
            ("view_txdtipodenuncia", "Can see available tipodenuncia"),
        )
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
    token = models.ForeignKey(TxdToken, models.DO_NOTHING, db_column='Token_id')  # Field name made lowercase.
    latitud= models.FloatField(blank=True, null=True)
    longitud= models.FloatField(blank=True, null=True)
    class Meta:
        permissions = (
            ("view_txddenuncia", "Can see available denuncia"),
        )
        db_table = 'txd_denuncia'

class TxdHorario(models.Model):
    idhorario = models.AutoField(db_column='idHorario', primary_key=True)  # Field name made lowercase.
    horainicio = models.TimeField()
    horafin = models.TimeField()
    duenio = models.ForeignKey(TxdDuenio, models.DO_NOTHING, db_column='Duenio_id')  # Field name made lowercase
    class Meta:
        permissions = (
            ("view_txdhorario", "Can see available horario"),
        )
        db_table = 'txd_horario'


class TxdHorariodetalle(models.Model):
    idhorariodetalle = models.AutoField(db_column='idHorarioDetalle', primary_key=True)  # Field name made lowercase.
    bus = models.ForeignKey(TxdBus, models.DO_NOTHING, db_column='Bus_id')  # Field name made lowercase.
    chofer = models.ForeignKey(TxdChofer, models.DO_NOTHING, db_column='Chofer_id')  # Field name made lowercase.
    horario = models.ForeignKey(TxdHorario, models.DO_NOTHING, db_column='Horario_id')  # Field name made lowercase.
    fecha = models.DateField()
    estado = models.IntegerField(blank=True, null=True)
    class Meta:
        permissions = (
            ("view_txdhorariodetalle", "Can see available horariodetalle"),
        )
        db_table = 'txd_horariodetalle'


class TxdRecurso(models.Model):
    idrecurso = models.AutoField(db_column='idRecurso', primary_key=True)  # Field name made lowercase.
    direccion = models.ImageField(upload_to='recurso/')
    denuncia = models.ForeignKey(TxdDenuncia, models.DO_NOTHING, db_column='Denuncia_id')  # Field name made lowercase.

    class Meta:
        permissions = (
            ("view_txdrecurso", "Can see available recurso"),
        )
        db_table = 'txd_recurso'


class TxuRol(models.Model):
    idrol = models.AutoField(db_column='idRol', primary_key=True)  # Field name made lowercase.
    rol = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        permissions = (
            ("view_txurol", "Can see available rol"),
        )
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
        permissions = (
            ("view_txuusuario", "Can see available usuario"),
        )
        db_table = 'txu_usuario'
