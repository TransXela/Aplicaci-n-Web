from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth.models import User,Group
from app.serializables import UserSerializer
from app.models import TxdDuenio
from app.serializables import TxdDuenioS
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.core.exceptions import ObjectDoesNotExist
from app import permisos
from app.vistas import autentificacion

@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication,))
@permission_classes((IsAuthenticated,))
def autenticar(request, tk, format=None):

    """
    Este metodo devuelve los datos de un usuario que se esta logeando
    """
    usuario = autentificacion.autenticacion(tk)
    if usuario.has_perms(permisos.duenios):
        if request.method == 'GET':
            try:
                objetoUsuario = User.objects.get(username=request.user)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            duenio = TxdDuenio.objects.get(usuario=objetoUsuario.id)
            serializador = TxdDuenioS(duenio)
            return Response(serializador.data)
    else:
        return Response("No tiene los permisos necesarios", status=status.HTTP_403_NOT_FOUND)




        """
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(content)
        """


@api_view(['POST'])
def crear_usuario(request, tk):
    """
    este metodo crea un nuevo usuario y retorna los datos creados
    """
    usuario = autentificacion.autenticacion(tk)
    if usuario.has_perms(permisos.duenios):
        if request.method == 'POST':
            serializador = UserSerializer(data = request.data)
            if serializador.is_valid():
                user = User.objects.create_user(username=request.data.get('username'),
                                                email=request.data.get('email'),
                                                password=request.data.get('password'))
                user.save()
                if 'idgroup' in request.data:
                    try:
                        grupo = Group.objects.get(pk=request.data['idgroup'])
                        user.groups.add(grupo)
                    except ObjectDoesNotExist:
                        n=0

                return Response(UserSerializer(User.objects.get(username=user)).data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("No tiene los permisos necesarios", status=status.HTTP_403_NOT_FOUND)

@api_view(['GET', 'PUT','DELETE'])
def detalle_usuario(request, pk, tk):
        """
        Actualiza, elimina un objeto segun su id
        """
        usuario = autentificacion.autenticacion(tk)
        if usuario.has_perms(permisos.duenios):
            try:
                obUsuario =  User.objects.get(pk = pk)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            if request.method == 'GET':
                serUsuario = UserSerializer(obUsuario)
                return Response(serUsuario.data)

            elif request.method == 'PUT':
                serUsuario = UserSerializer(obUsuario, data=request.data)
                if serUsuario.is_valid():
                    serUsuario.save()
                    user = User.objects.get(username=request.data.get('username'))
                    user.set_password(request.data.get('password'))
                    user.save()
                    return Response(serUsuario.data)
                return Response(serUsuario.errors,status=status.HTTP_400_BAD_REQUEST)

            elif request.method == 'DELETE':
                objeto.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("No tiene los permisos necesarios", status=status.HTTP_403_NOT_FOUND)

@api_view(['GET'])
def lista_usuario(request,tk):
        """
        Actualiza, elimina un objeto segun su id
        """
        usuario = autentificacion.autenticacion(tk)
        if usuario.has_perms(permisos.duenios):
            try:
                obUsuario =  User.objects.all()
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            if request.method == 'GET':
                serUsuario = UserSerializer(obUsuario,many=True)
                return Response(serUsuario.data)
        else:
            return Response("No tiene los permisos necesarios", status=status.HTTP_403_NOT_FOUND)

@api_view(['GET'])
def Usuarios_Group(request, pk, tk):
        """
        Actualiza, elimina un objeto segun su id
        """
        usuario = autentificacion.autenticacion(tk)
        if usuario.has_perms(permisos.duenios):
            try:
                usuarios = User.objects.filter(groups=pk)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            if request.method == 'GET':
                serializador = UserSerializer(usuarios, many=True)
                return Response(serializador.data)
            else:
                return Response(serUsuario.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("No tiene los permisos necesarios", status=status.HTTP_403_NOT_FOUND)

@api_view(['GET', 'PUT','DELETE'])
def CambiarEstado(request, pk, var, tk):
        """
        Actualiza, elimina un objeto segun su id
        """
        usuario = autentificacion.autenticacion(tk)
        if usuario.has_perms(permisos.duenios):
            try:
                obUsuario =  User.objects.get(pk=pk)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            if request.method == 'PUT':
                if(var==0):
                    U = UserSerializer(obUsuario)
                    dato = U.data
                    dato['is_active']=True
                    serUsuario = UserSerializer(obUsuario, data=dato)
                    if serUsuario.is_valid():
                        serUsuario.save()
                        return Response(serUsuario.data)
                    else:
                        return Response(serUsuario.errors,status=status.HTTP_400_BAD_REQUEST)
                elif(var==1):
                    U = UserSerializer(obUsuario)
                    dato = U.data
                    dato['is_active']=False
                    serUsuario = UserSerializer(obUsuario, data=dato)
                    if serUsuario.is_valid():
                        serUsuario.save()
                        return Response(serUsuario.data)
                    else:
                        return Response(serUsuario.errors,status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("No tiene los permisos necesarios", status=status.HTTP_403_NOT_FOUND)

@api_view(['GET', 'PUT','DELETE'])
def cambiarGrupo(request, pk, tk):
        """
        Actualiza, elimina un objeto segun su id
        """
        usuario = autentificacion.autenticacion(tk)
        if usuario.has_perms(permisos.duenios):
            try:
                obUsuario =  User.objects.get(pk = pk)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            if request.method == 'PUT':
                if "idGrupoNuevo" in request.data:
                    serUsuario = UserSerializer(obUsuario)
                    user=serUsuario.data
                    grupos=user['groups']
                    if len(grupos)!=0:
                        try:
                            grupoactual= Group.objects.get(pk=grupos[0])
                            obUsuario.groups.remove(grupoactual)
                        except ObjectDoesNotExist:
                             grupoactual=0
                    try:
                        gruponuevo= Group.objects.get(pk=request.data['idGrupoNuevo'])
                        obUsuario.groups.add(gruponuevo)
                    except ObjectDoesNotExist:
                        gruponuevo=0

                    serUsuario = UserSerializer(obUsuario)
                    return Response(serUsuario.data)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("No tiene los permisos necesarios", status=status.HTTP_403_NOT_FOUND)
