from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser, UserSession
from .serializers import UserSerializer, UserRegistrationSerializer
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from products.models import Product
from reports.models import WhatsAppReport

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        if user.is_active:
            login(request, user)
            
            # Registrar sesión
            UserSession.objects.create(
                user=user,
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            serializer = UserSerializer(user)
            return Response({
                'message': 'Login exitoso',
                'user': serializer.data
            })
        else:
            return Response(
                {'error': 'Cuenta desactivada'}, 
                status=status.HTTP_403_FORBIDDEN
            )
    else:
        return Response(
            {'error': 'Credenciales inválidas'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    # Marcar sesión como inactiva
    session = UserSession.objects.filter(
        user=request.user, 
        is_active=True
    ).last()
    
    if session:
        session.is_active = False
        session.save()
    
    logout(request)
    return Response({'message': 'Logout exitoso'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'message': 'Usuario registrado exitosamente',
            'user_id': user.id
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
@login_required
def dashboard_view(request):
    # Obtener estadísticas
    products_count = Product.objects.count()
    producers_count = Product.objects.values('producer_name').distinct().count()
    communities_count = Product.objects.values('community').distinct().count()
    pending_reports = WhatsAppReport.objects.filter(processed=False).count()
    
    # Productos recientes
    recent_products = Product.objects.all().order_by('-created_at')[:5]
    
    # Reportes de WhatsApp recientes
    recent_whatsapp_reports = WhatsAppReport.objects.all().order_by('-received_at')[:5]
    
    context = {
        'products_count': products_count,
        'producers_count': producers_count,
        'communities_count': communities_count,
        'pending_reports': pending_reports,
        'recent_products': recent_products,
        'recent_whatsapp_reports': recent_whatsapp_reports,
    }
    
    return render(request, 'admin/dashboard.html', context)