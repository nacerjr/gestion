from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db import transaction
import logging
from .models import User
from .serializers import (
    UserSerializer, 
    UserCreateSerializer, 
    CustomTokenObtainPairSerializer,
    LoginSerializer
)

logger = logging.getLogger(__name__)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        logger.info(f"Tentative de connexion pour: {request.data.get('email')}")
        
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            logger.error(f"Erreur de validation: {str(e)}")
            return Response({
                'error': 'Email ou mot de passe incorrect',
                'details': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Récupérer l'utilisateur
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        
        if not user:
            logger.error(f"Utilisateur non trouvé: {email}")
            return Response({
                'error': 'Utilisateur non trouvé'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Générer les tokens
        refresh = RefreshToken.for_user(user)
        
        logger.info(f"Connexion réussie pour: {email}")
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        })

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all().order_by('-created_at')
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserSerializer
    
    def perform_create(self, serializer):
        logger.info(f"Création d'utilisateur: {serializer.validated_data.get('email')}")
        try:
            with transaction.atomic():
                user = serializer.save()
                logger.info(f"Utilisateur créé avec succès: {user.email}")
        except Exception as e:
            logger.error(f"Erreur lors de la création d'utilisateur: {str(e)}")
            raise

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserCreateSerializer
        return UserSerializer
    
    def perform_update(self, serializer):
        logger.info(f"Modification d'utilisateur: {serializer.instance.email}")
        try:
            with transaction.atomic():
                user = serializer.save()
                logger.info(f"Utilisateur modifié avec succès: {user.email}")
        except Exception as e:
            logger.error(f"Erreur lors de la modification d'utilisateur: {str(e)}")
            raise

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def current_user_view(request):
    """Récupérer les informations de l'utilisateur connecté"""
    try:
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de l'utilisateur: {str(e)}")
        return Response({
            'error': 'Erreur lors de la récupération des données utilisateur'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """Déconnexion avec blacklist du refresh token"""
    try:
        refresh_token = request.data.get("refresh")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info(f"Déconnexion réussie pour: {request.user.email}")
        return Response({"message": "Déconnexion réussie"}, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Erreur lors de la déconnexion: {str(e)}")
        return Response({"error": "Token invalide"}, status=status.HTTP_400_BAD_REQUEST)