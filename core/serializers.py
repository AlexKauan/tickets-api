from rest_framework import serializers
from django.utils import timezone
from .models import Event, Customer, Ticket, Notification


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"
        read_only_fields = ("purchased_at", "created_at")

    def validate(self, attrs):
        status = attrs.get("status", getattr(self.instance, "status", None))
        customer = attrs.get("customer", getattr(self.instance, "customer", None))
        if status == Ticket.Status.SOLD and not customer:
            raise serializers.ValidationError("Ticket vendido deve estar associado a um cliente.")
        return attrs

    def update(self, instance, validated_data):
        prev_status = instance.status
        inst = super().update(instance, validated_data)
        if prev_status != Ticket.Status.SOLD and inst.status == Ticket.Status.SOLD:
            inst.purchased_at = timezone.now()
            inst.save(update_fields=["purchased_at"])
        return inst


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
        read_only_fields = ("sent_at", "created_at")
