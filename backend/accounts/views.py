from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.contrib.auth import authenticate
from .models import User
from .serializers import (
    UserSerializer, 
    UserCreateSerializer, 
    CustomTokenObtainPairSerializer,
    LoginSerializer
)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({
                'error': 'Email ou mot de passe incorrect',
                'details': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Récupérer l'utilisateur
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        
        if not user:
            return Response({
                'error': 'Utilisateur non trouvé'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Générer les tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        })

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """Vue de login alternative utilisant le serializer custom"""
    serializer = CustomTokenObtainPairSerializer(data=request.data)
    
    try:
        serializer.is_valid(raise_exception=True)
        
        # Récupérer l'utilisateur
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        
        if not user:
            return Response({
                'error': 'Utilisateur non trouvé'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Générer les tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        })
        
    except Exception as e:
        return Response({
            'error': 'Email ou mot de passe incorrect',
            'details': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def current_user_view(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    try:
        refresh_token = request.data.get("refresh")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response({"message": "Déconnexion réussie"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": "Token invalide"}, status=status.HTTP_400_BAD_REQUEST)