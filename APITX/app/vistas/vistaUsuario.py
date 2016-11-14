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
from rest_framework.authtoken.models import Token


@api_view(['POST'])
def crear_usuario(request):
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
        if usuario.has_perm('auth.add_user'):
            serializador = UserSerializer(data = request.data)
            if serializador.is_valid():
                serializador.save()
                ultimoId = User.objects.latest('id')
                user= User.objects.get(pk=ultimoId.id)

                if 'idgroup' in request.data:
                    try:
                        grupo = Group.objects.get(pk=request.data['idgroup'])
                        user.groups.add(grupo)
                    except ObjectDoesNotExist:
                        n=0
                try:
                    objetoUsuario = User.objects.get(pk=user.id)
                except ObjectDoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)

                data = {"id":user.id ,"username":user.username, "email": user.email, "password" :user.password}
                serializador = UserSerializer(objetoUsuario)
                return Response(serializador.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            content = {'Permiso denegado': 'El usuario no tiene permisos para ingresar datos'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)

    return Response(status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT','DELETE'])
def detalle_usuario(request, pk):
        """
        Actualiza, elimina un objeto segun su id
        """
        try:
            objToken = Token.objects.get(key=request.query_params.get('tk'))
            usuario = User.objects.get(pk=objToken.user.id)
        except ObjectDoesNotExist:
            content = {'Datos incorrectos': 'El token enviado no coincide para ningun usuario'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)

        try:
            obUsuario =  User.objects.get(pk = pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            if usuario.has_perm('app.view_txdpmt') | usuario.has_perm('app.view_txdduenio') | usuario.has_perm('app.view_txccultura'):
                serUsuario = UserSerializer(obUsuario)
                return Response(serUsuario.data)
            else:
                content = {'Permiso denegado': 'El usuario no tiene permisos para ver los datos'}
                return Response(content, status=status.HTTP_403_FORBIDDEN)

        elif request.method == 'PUT':
            if usuario.has_perm('auth.change_user'):
                serUsuario = UserSerializer(obUsuario, data=request.data)
                if serUsuario.is_valid():
                    serUsuario.save()
                    user = User.objects.get(username=request.data.get('username'))
                    user.save()
                    return Response(serUsuario.data)
                return Response(serUsuario.errors,status=status.HTTP_400_BAD_REQUEST)
            else:
                content = {'Permiso denegado': 'El usuario no tiene permisos para editar datos'}
                return Response(content, status=status.HTTP_403_FORBIDDEN)


        elif request.method == 'DELETE':
            if usuario.has_perm('auth.delete_user'):
                objeto.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                content = {'Permiso denegado': 'El usuario no tiene permisos para eliminar datos'}
                return Response(content, status=status.HTTP_403_FORBIDDEN)



@api_view(['GET','POST'])
def lista_usuario(request):
        """
        Actualiza, elimina un objeto segun su id
        """
        try:
            objToken = Token.objects.get(key=request.query_params.get('tk'))
            usuario = User.objects.get(pk=objToken.user.id)
        except ObjectDoesNotExist:
            content = {'Datos incorrectos': 'El token enviado no coincide para ningun usuario'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)


        obUsuario =  User.objects.all()
        if request.method == 'GET':
            if usuario.has_perm('app.view_txdpmt') | usuario.has_perm('app.view_txdduenio') | usuario.has_perm('app.view_txccultura'):
                serUsuario = UserSerializer(obUsuario,many=True)
                return Response(serUsuario.data)
            else:
                content = {'Permiso denegado': 'El usuario no tiene permisos para ver los datos'}
                return Response(content, status=status.HTTP_403_FORBIDDEN)

        elif request.method == 'POST':
            if usuario.has_perm('auth.add_user'):
                serializador = UserSerializer(data = request.data)
                if serializador.is_valid():
                    user = User.objects.create_user(username=request.data.get('username'),
                                                email=request.data.get('email'),
                                                password=request.data.get('password'))
                    if "is_active" in request.data:
                        user.is_active=request.data.get('is_active')
                    if "is_staff" in request.data:
                        user.is_staff=request.data.get('is_staff')
                    if "is_superuser" in request.data:
                        user.is_superuser=request.data.get('is_superuser')

                    user.save()
                    if 'idgroup' in request.data:
                        try:
                            grupo = Group.objects.get(pk=request.data['idgroup'])
                            user.groups.add(grupo)
                        except ObjectDoesNotExist:
                            n=0
                    serializador = UserSerializer(user)
                    return Response(serializador.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializador.errors,status=status.HTTP_400_BAD_REQUEST)
            else:
                content = {'Permiso denegado': 'El usuario no tiene permisos para ingresar datos'}
                return Response(content, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def Usuarios_Group(request, pk):
        """
        Actualiza, elimina un objeto segun su id
        """
        try:
            objToken = Token.objects.get(key=request.query_params.get('tk'))
            usuario = User.objects.get(pk=objToken.user.id)
        except ObjectDoesNotExist:
            content = {'Datos incorrectos': 'El token enviado no coincide para ningun usuario'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)

        if request.method == 'GET':
            if usuario.has_perm('app.view_txdpmt') | usuario.has_perm('app.view_txdduenio') | usuario.has_perm('app.view_txccultura'):
                try:
                    usuarios = User.objects.filter(groups=pk)
                except ObjectDoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)

                serializador = UserSerializer(usuarios, many=True)
                return Response(serializador.data)
            else:
                content = {'Permiso denegado': 'El usuario no tiene permisos para ver los datos'}
                return Response(content, status=status.HTTP_403_FORBIDDEN)

        else:
            return Response(serUsuario.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def CambiarEstado(request, pk, var):
        """
        Actualiza, elimina un objeto segun su id
        """
        try:
            objToken = Token.objects.get(key=request.query_params.get('tk'))
            usuario = User.objects.get(pk=objToken.user.id)
        except ObjectDoesNotExist:
            content = {'Datos incorrectos': 'El token enviado no coincide para ningun usuario'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)

        try:
            obUsuario =  User.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'PUT':
            if usuario.has_perms('auth.change_user'):
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
                content = {'Permiso denegado': 'El usuario no tiene permisos para editar datos'}
                return Response(content, status=status.HTTP_403_FORBIDDEN)



@api_view(['PUT'])
def cambiarGrupo(request, pk):
        """
        Actualiza, elimina un objeto segun su id
        """
        try:
            objToken = Token.objects.get(key=request.query_params.get('tk'))
            usuario = User.objects.get(pk=objToken.user.id)
        except ObjectDoesNotExist:
            content = {'Datos incorrectos': 'El token enviado no coincide para ningun usuario'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)

        try:
            obUsuario =  User.objects.get(pk = pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'PUT':
            if usuario.has_perm('auth.change_user'):
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
                content = {'Permiso denegado': 'El usuario no tiene permisos para editar datos'}
                return Response(content, status=status.HTTP_403_FORBIDDEN)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def cambiarContrasenia(request, pk):
        """
        Actualiza, elimina un objeto segun su id
        """
        try:
            objToken = Token.objects.get(key=request.query_params.get('tk'))
            usuario = User.objects.get(pk=objToken.user.id)
        except ObjectDoesNotExist:
            content = {'Datos incorrectos': 'El token enviado no coincide para ningun usuario'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)

        try:
            obUsuario =  User.objects.get(pk = pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'PUT':
            if usuario.has_perm('auth.change_user'):
                if "password" in request.data:
                    obUsuario.set_password(request.data['password'])
                    obUsuario.save()
                    serializador = UserSerializer(obUsuario)
                    return Response(serializador.data, status=status.HTTP_201_CREATED)
                else :
                    Response(status=status.HTTP_400_BAD_REQUEST)


            else:
                content = {'Permiso denegado': 'El usuario no tiene permisos para editar datos'}
                return Response(content, status=status.HTTP_403_FORBIDDEN)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def cambiarContreniaUsuario(request, pk):
        """
        Actualiza, elimina un objeto segun su id
        """
        try:
            objToken = Token.objects.get(key=request.query_params.get('tk'))
            usuario = User.objects.get(pk=objToken.user.id)
        except ObjectDoesNotExist:
            content = {'Datos incorrectos': 'El token enviado no coincide para ningun usuario'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)

        try:
            obUsuario =  User.objects.get(pk = pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'PUT':
            if usuario.has_perm('auth.change_user'):
                if "password_old" in request.data and "password_new" in request.data:
                    if obUsuario .check_password(request.data['password_old']):
                        obUsuario .set_password(request.data['password_new'])
                        obUsuario.save()
                        serializador = UserSerializer(obUsuario )
                        return Response(serializador.data, status=status.HTTP_201_CREATED)
                    else:
                        return Response(status=status.HTTP_400_BAD_REQUEST)

                else :
                    content = {'Permiso denegado': 'la contrasenia es invalida'}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)


            else:
                content = {'Permiso denegado': 'El usuario no tiene permisos para editar datos'}
                return Response(content, status=status.HTTP_403_FORBIDDEN)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
