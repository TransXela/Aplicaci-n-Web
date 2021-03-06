# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-10 00:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20161022_1759'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='txcactividad',
            options={'permissions': (('view_txcactividad', 'Can see available actividad'),)},
        ),
        migrations.AlterModelOptions(
            name='txcarticulo',
            options={'permissions': (('view_txcarticulo', 'Can see available articulo'),)},
        ),
        migrations.AlterModelOptions(
            name='txccapitulo',
            options={'permissions': (('view_txccapitulo', 'Can see available capitulo'),)},
        ),
        migrations.AlterModelOptions(
            name='txccultura',
            options={'permissions': (('view_txccultura', 'Can see available cultura'),)},
        ),
        migrations.AlterModelOptions(
            name='txcoconsejo',
            options={'permissions': (('view_txcoconsejo', 'Can see available consejo'),)},
        ),
        migrations.AlterModelOptions(
            name='txcofecha',
            options={'permissions': (('view_txcofecha', 'Can see available fecha'),)},
        ),
        migrations.AlterModelOptions(
            name='txcpregunta',
            options={'permissions': (('view_txcpregunta', 'Can see available pregunta'),)},
        ),
        migrations.AlterModelOptions(
            name='txcpreguntaarticulo',
            options={'permissions': (('view_txcpreguntaarticulo', 'Can see available txcpreguntaarticulo'),)},
        ),
        migrations.AlterModelOptions(
            name='txctitulo',
            options={'permissions': (('view_txctitulo', 'Can see available titulo'),)},
        ),
        migrations.AlterModelOptions(
            name='txdbus',
            options={'permissions': (('view_txdbus', 'Can see available bus'),)},
        ),
        migrations.AlterModelOptions(
            name='txdchofer',
            options={'permissions': (('view_txdchofer', 'Can see available chofer'),)},
        ),
        migrations.AlterModelOptions(
            name='txddenuncia',
            options={'permissions': (('view_txddenuncia', 'Can see available denuncia'),)},
        ),
        migrations.AlterModelOptions(
            name='txdduenio',
            options={'permissions': (('view_txdduenio', 'Can see available duenio'),)},
        ),
        migrations.AlterModelOptions(
            name='txdhorario',
            options={'permissions': (('view_txdhorario', 'Can see available horario'),)},
        ),
        migrations.AlterModelOptions(
            name='txdhorariodetalle',
            options={'permissions': (('view_txdhorariodetalle', 'Can see available horariodetalle'),)},
        ),
        migrations.AlterModelOptions(
            name='txdpmt',
            options={'permissions': (('view_txdpmt', 'Can see available pmt'),)},
        ),
        migrations.AlterModelOptions(
            name='txdrecurso',
            options={'permissions': (('view_txdrecurso', 'Can see available recurso'),)},
        ),
        migrations.AlterModelOptions(
            name='txdruta',
            options={'permissions': (('view_txdruta', 'Can see available ruta'),)},
        ),
        migrations.AlterModelOptions(
            name='txdtipodenuncia',
            options={'permissions': (('view_txdtipodenuncia', 'Can see available tipodenuncia'),)},
        ),
        migrations.AlterModelOptions(
            name='txdtoken',
            options={'permissions': (('view_txdtoken', 'Can see available Token'),)},
        ),
        migrations.AlterModelOptions(
            name='txurol',
            options={'permissions': (('view_txurol', 'Can see available rol'),)},
        ),
        migrations.AlterModelOptions(
            name='txuusuario',
            options={'permissions': (('view_txuusuario', 'Can see available usuario'),)},
        ),
    ]
