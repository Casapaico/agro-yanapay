from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def price_predictions(request):
    # Placeholder para predicciones de precios
    return Response({
        'message': 'Módulo de predicción de precios - En desarrollo',
        'predictions': []
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def production_analysis(request):
    # Placeholder para análisis de producción
    return Response({
        'message': 'Módulo de análisis de producción - En desarrollo',
        'analysis': {}
    })