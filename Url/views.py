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
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

def set_token_cookie(response,token):
    response.set_cookie('auth_token', token, httponly=True, secure=True)

class UserViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    @action(detail=False,methods=['post'],url_path='signup')
    def signup(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save() #Crée l'utilisateur
            response = Response({
                'message': "Inscritpon réussi",
                'username': user.username
            }, status=status.HTTP_201_CREATED)

            # set_token_cookie(response,token.key)

            return response
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

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
                # Générer ou récupérer un token pour l'utisateur
                token, created = Token.objects.get_or_create(user=user)
                
                response = Response({"message":"connexion réussie.", "token": token.key}, status=status.HTTP_200_OK)
            
            else:
                return Response({"message": "Nom d'utilisateur ou mot de passe incorrect"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

   


    
class ClickViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated] # Seuls les utilisateurs authentifier quie peuvent se connecter
    queryset = Click.objects.all()
    serializer_class = ClickSerializer

    @action(detail=False,methods=['post'], url_path='create')
    def generate_url(self,request):
        # Méthode pour permetre d'enregistrer une  URL et générer une URL de suivi
        use_c = request.user
        print("**************")
        print(use_c, "***************")
        print('**************')
        url = request.data.get('url') # Réccupére l'URL d'origine
        current_user = request.data.get('user') # Réccupérre user
        user = User.objects.get(email=current_user) 
        if not url:
            return Response({'error': "URL is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Enrégister L'URL dans la base de données avec un code unique
        click = Click.objects.create(user=user,url=url)

        # Retourner une URL de suivi à partager
        follow_url = f"http://127.0.0.1:8000/clicks/{click.unique_code}/track/"
        click.url_output = follow_url 
        click.save()
        return Response({'follow_url': follow_url}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], url_path='track')
    def track(self,request,pk=None):

        print( "*******************************")
        # cette action suit les clics sur l'URL et redirige vers l'URL d'origin.abs
        try:
            click = Click.objects.get(unique_code=pk)
            click.clicks += 1
            click.save()

            # Rediriger l'utilisateurs vers l'URL d'origine
            return redirect(click.url)
        except Click.DoesNotExist:
            return Response({"error": "URL not found"}, status=status.HTTP_404_NOT_FOUND)


  