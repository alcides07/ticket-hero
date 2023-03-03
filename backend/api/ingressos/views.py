from django.http import request
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from .permissions import AllowAny
from .models import Cliente, Organizador, Evento, Categoria, Compra
from .serializers import ClienteSerializer, OrganizadorSerializer, EventoSerializer, CategoriaSerializer, CompraSerializer, CadastroSerializer, LoginSerializer

class Auth(viewsets.ViewSet):
    serializer_class = None 

    @action(detail=False, methods=["post"], basename="auth", permission_classes=[AllowAny])
    def login(self, request):
        usuario = User.objects.filter(username=request.data.get("usuario"))

        if not usuario.exists():
            usuario = User.objects.filter(email=request.data.get("email"))
            if not usuario.exists():
                return Response({"erro":"Credenciais inválidas!"}, status=status.HTTP_400_BAD_REQUEST)

        usuario = usuario.first()
        if not usuario.check_password(request.data.get("senha")):
            return Response({"erro": "Credenciais inválidas!"}, status=status.HTTP_400_BAD_REQUEST)

        token = Token.objects.create(user=usuario)        
        serializer = LoginSerializer(usuario).data
        serializer ['token'] = token.key
        return Response(serializer, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], basename="auth", permission_classes=[AllowAny])
    def cadastro(self, request):
        username = request.data.get("usuario")
        senha = request.data.get("senha")
        confirmacaoSenha = request.data.get("confirmacaoSenha")
        tipoUsuario = request.data.get("tipoUsuario")
        nomeCompleto = request.data.get("nomeCompleto")
        email = request.data.get("email")
        nascimento = request.data.get("nascimento")

        if (senha != confirmacaoSenha):
            return Response({"erro": "Senhas não coincidem!"}, status=status.HTTP_400_BAD_REQUEST)

        if (User.objects.filter(username = username)):
            return Response({"erro": "Esse nome de usuário já está em uso!"}, status=status.HTTP_400_BAD_REQUEST)
    
        if (User.objects.filter(email = email)):
            return Response({"erro": "Esse e-mail já está em uso!"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=senha)

        if (tipoUsuario.upper() == "O"):
            organizador = Organizador.objects.create(user=user, nomeCompleto=nomeCompleto, nascimento=nascimento)
            usuario = organizador

        elif (tipoUsuario.upper() == "C"):
            cliente = Cliente.objects.create(user=user, nomeCompleto=nomeCompleto, nascimento=nascimento)
            usuario = cliente
        
        serializer = CadastroSerializer(usuario)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ClienteViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class OrganizadorViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Organizador.objects.all()
    serializer_class = OrganizadorSerializer

class EventoViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class VendaViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer

    def create(self, request):  
        qtdIngresso = int(request.data.get("qtdIngresso"))
        evento = get_object_or_404(Evento, id = request.data.get("evento"))

        if (qtdIngresso <= evento.ingressoDisponivel):
            venda = Compra.objects.create(
                qtdIngresso = qtdIngresso,
                valorTotal = qtdIngresso * evento.valorIngresso,
                dataCompra = timezone.now(),
                cliente = get_object_or_404(Cliente, id = request.data.get("cliente")),
                evento = evento
            )
            
            evento.ingressoDisponivel -= venda.qtdIngresso
            evento.save()
            serializer = CompraSerializer(venda)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"Erro":"Ingressos insuficientes"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], permission_classes = [permissions.IsAuthenticated])
    def minhasCompras(self, request):
        queryset = Compra.objects.filter(cliente = request.user.cliente)
        contexto = {}
        i = 1

        for ingresso in queryset:
            serializer = CompraSerializer(ingresso)

            contexto[f"ingresso {i}"] = {
                "ingresso" : serializer.data,
                "evento" : {
                    "id": ingresso.evento.id,
                    "nome": ingresso.evento.nome,
                    "descricao": ingresso.evento.descricao,
                    "data": ingresso.evento.data,
                    "categoria" : ingresso.evento.categoria.nome,
                    "organizador": ingresso.evento.organizador.nomeCompleto                
                }
            }
            i += 1

        '''
        MODO 2 - TENTATIVA

        queryset = Compra.objects.filter(cliente = request.user.cliente)
        contexto = {}
 
        for ingresso in queryset:
            serializer = CompraSerializer(ingresso)

            contextoAtual = {
                "Ingressos" : serializer.data,
                "Evento" : {
                    "nome" : ingresso.evento.nome,
                    "data" : ingresso.evento.data,
                    "categoria" : ingresso.evento.categoria.nome
                }
            }

            # Comprei um outro ingresso para um mesmo evento
            if (ingresso.evento.id in contexto):
                ingressosExistentesDicionario = contexto[ingresso.evento.id]["Ingressos"]
                ingressosExistentesLista = []

                for i in ingressosExistentesDicionario:
                    ingressosExistentesLista.append(i)
                ingressosExistentesLista.append(serializer.data)

                contexto[ingresso.evento.id]["Ingressos"] = ingressosExistentesLista

            # Possuo um ingresso para um evento que nunca comprei antes
            else:
                contexto[ingresso.evento.id] = contextoAtual
        '''

        return Response(contexto, status=status.HTTP_200_OK)