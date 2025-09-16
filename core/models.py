from django.db import models
from django.utils import timezone


class Event(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    capacity = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["start_datetime"]

    def __str__(self):
        return f"{self.title} @ {self.start_datetime:%d/%m/%Y %H:%M}"


class Customer(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Ticket(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "AVAILABLE", "Disponível"
        RESERVED = "RESERVED", "Reservado"
        SOLD = "SOLD", "Vendido"

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="tickets")
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name="tickets"
    )
    code = models.CharField(max_length=30, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.AVAILABLE
    )
    purchased_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["event", "code"]

    def __str__(self):
        return f"{self.code} - {self.event.title}"


class Notification(models.Model):
    class Channel(models.TextChoices):
        EMAIL = "EMAIL", "Email"
        SMS = "SMS", "SMS"
        INAPP = "INAPP", "In-App"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pendente"
        SENT = "SENT", "Enviada"
        FAILED = "FAILED", "Falhou"

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=120)
    message = models.TextField()
    channel = models.CharField(max_length=10, choices=Channel.choices, default=Channel.EMAIL)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    sent_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def mark_sent(self):
        self.status = self.Status.SENT
        self.sent_at = timezone.now()
        self.save(update_fields=["status", "sent_at"])

    def __str__(self):
        return f"[{self.status}] {self.title} -> {self.customer.name}"
