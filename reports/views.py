from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import ProductionReport, WhatsAppReport

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def production_reports(request):
    reports = ProductionReport.objects.all().order_by('-generated_at')
    data = [
        {
            'id': report.id,
            'title': report.title,
            'report_type': report.report_type,
            'period_start': report.period_start,
            'period_end': report.period_end,
            'total_production_kg': report.total_production_kg,
            'total_value': report.total_value,
            'generated_by': report.generated_by.username,
            'generated_at': report.generated_at,
        }
        for report in reports
    ]
    return Response(data)

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
            'received_at': report.received_at,
            'processed': report.processed,
        }
        for report in reports
    ]
    return Response(data)