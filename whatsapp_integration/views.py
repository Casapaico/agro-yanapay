from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import WhatsAppReport

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def whatsapp_reports(request):
    reports = WhatsAppReport.objects.all().order_by('-received_at')
    data = [
        {
            'id': report.id,
            'producer_name': report.producer_name,
            'product_name': report.product_name,
            'volume_kg': report.volume_kg,
            'location': report.location,
            'availability_date': report.availability_date,
            'message_content': report.message_content,
            'received_at': report.received_at,
            'processed': report.processed,
        }
        for report in reports
    ]
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def process_report(request, report_id):
    try:
        report = WhatsAppReport.objects.get(id=report_id)
        report.processed = True
        report.processed_by = request.user
        report.save()
        return Response({'message': 'Reporte procesado correctamente'})
    except WhatsAppReport.DoesNotExist:
        return Response({'error': 'Reporte no encontrado'}, status=status.HTTP_404_NOT_FOUND)