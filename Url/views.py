from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import redirect
from .models import Click
from .serialiers import ClickSerializer, UserSerializer, LoginSerializer
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from .url import shorten_url


# Fonction pour enregistrer un nouveau user
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=False,methods=['post'],url_path='signup')
    def signup(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save() #Crée l'utilisateur
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user_auth = authenticate(request,username = username, password=password)

            if user_auth:
                login(request, user_auth)

                token, create = Token.objects.get_or_create(user=user_auth)

                response = Response({
                    'message': "Inscritpon réussi",
                    'username': user.username,
                    'token': token.key
                }, status=status.HTTP_201_CREATED)

            # set_token_cookie(response,token.key)

                return response
            else:
                return Response({"message": "Nom d'utilisateur ou mot de passe incorrect"},status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# Fonction pour loger l'utisateur qui a déja un compte
class UserLoginViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'], url_path='login')
    def login(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)

            if user:
                login(request,user)
                # Générer ou récupérer un token pour l'utisateur
                token, created = Token.objects.get_or_create(user=user)
                
                response =  Response({"message":"connexion réussie.", "token": token.key}, status=status.HTTP_200_OK)
                return response
            else:
                return Response({"message": "Nom d'utilisateur ou mot de passe incorrect"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


    
class ClickViewSet(viewsets.ViewSet):
    
    serializer_class = ClickSerializer

    # # Fonction pour personnaliser 
    # def get_queryset(self):
    #     # Récupére l'utilisateur connecté
    #     user = self.request.user
    #     if user.is_authenticated:
    #         return Click.objects.filter(user=user)
        
    #     return Click.objects.none() # Retourne un queryset vide si l'utisateur n'est pas authentifié
   
    @action(detail=False,methods=['get'],url_path='get_url')
    def get_url(self, request):
        current_user = self.request.user
        
        click = Click.objects.filter(user=current_user)

        serializer = ClickSerializer(click,many=True)

        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


    # Fonction pour géneré un url de track
    @action(detail=False,methods=['post'], url_path='create')
    def generate_url(self,request):
        # Méthode pour permetre d'enregistrer une  URL et générer une URL de suivi
        current_user = self.request.user
        url = request.data.get('url') # Réccupére l'URL d'origine
        serializer = ClickSerializer(data=request.data)
        if serializer.is_valid():
            link_name = serializer.validated_data['link_name']
            url = serializer.validated_data['url']

            # Enrégistreer L'URL dans la base de donnée avec un code unique
            click = Click.objects.create(user=current_user, link_name=link_name , url=url)
            
            # Retourner L'URL de suivi à partager
            url_output = f"http://127.0.0.1:8000/clicks/{click.unique_code}/track/"

            try:
           
                # Appel de la fonction pour racourcire l'url
                short_url = shorten_url(url_output)

                # Enrégistre l'url de sortie
        
                click.url_output = short_url
                click.save()
                return Response({"data": ClickSerializer(click).data}, status=status.HTTP_201_CREATED)
            except:
                
                click.url_output = url_output
                click.save()
                return Response({"data": ClickSerializer(click).data}, status=status.HTTP_201_CREATED)
        
     
        else:
            return Response({'error': "URL is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # # Enrégister L'URL dans la base de données avec un code unique
        # click = Click.objects.create(user=current_user,url=url)

        # Retourner une URL de suivi à partager
        # follow_url = f"http://127.0.0.1:8000/clicks/{click.unique_code}/track/"
        # click.url_output = follow_url 
        # click.save()
        # return Response({'follow_url': follow_url}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], url_path='track')
    def track(self,request,pk=None):

        # cette action suit les clics sur l'URL et redirige vers l'URL d'origin.abs
        try:
            click = Click.objects.get(unique_code=pk)
            click.clicks += 1
            click.save()

            # Rediriger l'utilisateurs vers l'URL d'origine
            return redirect(click.url)
        except Click.DoesNotExist:
            return Response({"error": "URL not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'], url_path='delete')
    def delete(self,request,pk=None):

        # Fonction pour suprimer les lien
        try: 
            link = Click.objects.get(unique_code=pk)
            link.delete()
            
            return Response({"success": "ok"}, status=status.HTTP_200_OK)
        except:
            return Response({'error': "URL not found"}, status=status.HTTP_404_NOT_FOUND)

        



  