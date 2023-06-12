from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .pdf_templates.order_pdf_template import generate_order_pdf
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from rest_framework.permissions import IsAuthenticated


def download_pdf_view(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    pdf = generate_order_pdf(order)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"attachment; filename=order_{order_id}.pdf"
    response.write(pdf)
    return response


class OrderListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.all().order_by("-created_at")
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, order_id):
        return get_object_or_404(Order, order_id=order_id)

    def get(self, request, order_id):
        order = self.get_object(order_id)
        serializer = OrderSerializer(order)
        order_data = serializer.data

        order_items = OrderItem.objects.filter(order=order)
        order_item_serializer = OrderItemSerializer(order_items, many=True)
        order_data["order_items"] = order_item_serializer.data

        return Response(order_data)

    def delete(self, request, order_id):
        order = self.get_object(order_id)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
