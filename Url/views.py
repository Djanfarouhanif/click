from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import redirect
from .models import Click
from .serialiers import ClickSerializer
from rest_framework.views import APIView
from rest_framework import status

class ClickViewSet(viewsets.ViewSet):

    @action(detail=False,methods=['post'], url_path='create')
    def generate_url(self,request):
        # Méthode pour permetre d'enregistrer une  URL et générer une URL de suivi

        url = request.data.get('url') # Réccupére l'URL d'origine

        if not url:
            return Response({'error': "URL is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Enrégister L'URL dans la base de données avec un code unique
        click = Click.objects.create(url=url)

        # Retourner une URL de suivi à partager
        follow_url = f"http://127.0.0.1:8000/clicks/track/{click.unique_code}/"
        return Response({'follow_url': follow_url}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], url_path='track')
    def track(self,request,unique_code=None):

        print(unique_code, "*******************************")
        # cette action suit les clics sur l'URL et redirige vers l'URL d'origin.abs
        try:
            click = Click.objects.get(unique_code=unique_code)
            click.clicks += 1
            click.save()

            # Rediriger l'utilisateurs vers l'URL d'origine
            return redirect(click.url)
        except Click.DoesNotExist:
            return Response({"error": "URL not found"}, status=status.HTTP_404_NOT_FOUND)


  