from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User,Group
from app.serializables import UserSerializer
from app.models import TxdDuenio, TxdPmt, TxcCultura
from app.serializables import TxdDuenioS, TxdPmtS, TxcCulturaS
from rest_framework.authtoken.models import Token

@api_view(['POST'])
def crear_usuarioPersona(request):
    """
    este metodo crea un nuevo usuario y retorna los datos creados
    """
    try:
        objToken = Token.objects.get(key=request.query_params.get('tk'))
        usuario = User.objects.get(pk=objToken.user.id)
    except ObjectDoesNotExist:
        content = {'Datos incorrectos': 'El token enviado no coincide para ningun usuario'}
        return Response(content, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'POST':
        if usuario.has_perms('auth.add_user'):

            serializador = list()

            usuario = {"username": request.data.get('username'), "email": request.data.get('email'),
                        "password": request.data.get('password')}
            serializadorUsuario = UserSerializer(data = usuario)
            if serializadorUsuario.is_valid():
                serializadorUsuario.save()
                ultimoId = User.objects.latest('id')
                user= User.objects.get(pk=ultimoId.id)
                user.set_password(request.data.get('password'))
                user.save()
                serializador+=[UserSerializer(user).data]
                if 'idgroup' in request.data:
                    try:
                        grupo = Group.objects.get(pk=request.data['idgroup'])
                        user.groups.add(grupo)
                    except ObjectDoesNotExist:
                        n=0
                persona = { "nombre": request.data.get('nombre'), "apellidos": request.data.get('apellidos'),
                            "direccion": request.data.get('direccion'), "dpi": request.data.get('dpi'),
                            "telefono": request.data.get('telefono'), "correo": request.data.get('email'),
                            "fecha_nac": request.data.get('fecha_nac'), "fecha_crea": request.data.get('fecha_crea'),
                            "estado": request.data.get('estado'), "empresa": request.data.get('empresa'),
                            "usuario": user.pk
                            }

                if grupo.name == 'duenios':
                    serializadorpersona = TxdDuenioS(data=persona)
                    if serializadorpersona.is_valid():
                        serializadorpersona.save()
                        serializador+= [serializadorpersona.data]
                    else:
                        return Response(serializadorpersona.errors, status=status.HTTP_400_BAD_REQUEST)

                elif grupo.name == 'pmt':
                    serializadorpersona = TxdPmtS(data=persona)
                    if serializadorpersona.is_valid():
                        serializadorpersona.save()
                        serializador+=[serializadorpersona.data]
                    else:
                        return Response(serializadorpersona.errors, status=status.HTTP_400_BAD_REQUEST)

                elif grupo.name == 'cultura':
                    serializadorpersona = TxcCulturaS(data=persona)
                    if serializadorpersona.is_valid():
                        serializadorpersona.save()
                        serializador+=[serializadorpersona.data]
                    else:
                        return Response(serializadorpersona.errors, status=status.HTTP_400_BAD_REQUEST)

                try:
                    objetoUsuario = User.objects.get(pk=user.id)
                except ObjectDoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)

                #data = {"id":user.id ,"username":user.username, "email": user.email, "password" :user.password}
                #serializador = UserSerializer(objetoUsuario)
                return Response(serializador, status=status.HTTP_201_CREATED)
            else:
                return Response(serializadorUsuario.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            content = {'Permiso denegado': 'El usuario no tiene permisos para ingresar datos'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)

    return Response(status=status.HTTP_400_BAD_REQUEST)
