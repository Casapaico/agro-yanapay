from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count, Sum, Avg
from .models import Product, ProductCategory
from .serializers import ProductSerializer, ProductCategorySerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def product_create(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def product_update(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Product.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def product_delete(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response({'message': 'Producto eliminado correctamente'})
    except Product.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def category_list(request):
    categories = ProductCategory.objects.filter(is_active=True)
    serializer = ProductCategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product_stats(request):
    stats = {
        'total_products': Product.objects.count(),
        'available_products': Product.objects.filter(status='available').count(),
        'total_kg_available': Product.objects.aggregate(total=Sum('available_kg'))['total'] or 0,
        'products_by_status': list(Product.objects.values('status').annotate(count=Count('id'))),
        'products_by_category': list(Product.objects.values('category__name').annotate(count=Count('id'), total_kg=Sum('available_kg'))),
    }
    return Response(stats)