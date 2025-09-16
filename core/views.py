from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from .models import Event, Customer, Ticket, Notification
from .serializers import (
    EventSerializer,
    CustomerSerializer,
    TicketSerializer,
    NotificationSerializer,
)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filterset_fields = ["location"]
    search_fields = ["title", "location"]
    ordering_fields = ["start_datetime", "end_datetime", "title"]


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filterset_fields = ["email"]
    search_fields = ["name", "email"]
    ordering_fields = ["name", "created_at"]


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.select_related("event", "customer").all()
    serializer_class = TicketSerializer
    filterset_fields = ["event", "status", "customer"]
    search_fields = ["code", "event__title", "customer__name"]
    ordering_fields = ["price", "code", "created_at"]

    @action(detail=True, methods=["post"])
    def mark_sold(self, request, pk=None):
        ticket = self.get_object()
        customer_id = request.data.get("customer")
        if not customer_id:
            return Response({"detail": "Informe 'customer'."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            return Response({"detail": "Cliente não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        ticket.customer = customer
        ticket.status = Ticket.Status.SOLD
        ticket.purchased_at = timezone.now()
        ticket.save()
        Notification.objects.create(
            customer=customer,
            title="Compra confirmada",
            message=f"Seu ingresso {ticket.code} para {ticket.event.title} foi confirmado.",
            channel=Notification.Channel.EMAIL,
            status=Notification.Status.PENDING,
        )
        return Response(self.get_serializer(ticket).data)


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.select_related("customer").all()
    serializer_class = NotificationSerializer
    filterset_fields = ["status", "channel", "customer"]
    search_fields = ["title", "message", "customer__name", "customer__email"]
    ordering_fields = ["created_at", "sent_at"]

    @action(detail=True, methods=["post"])
    def mark_sent(self, request, pk=None):
        notif = self.get_object()
        notif.mark_sent()
        return Response(self.get_serializer(notif).data)
