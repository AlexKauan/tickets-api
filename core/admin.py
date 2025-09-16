from django.contrib import admin
from .models import Event, Customer, Ticket, Notification

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "location", "start_datetime", "end_datetime", "capacity")
    search_fields = ("title", "location")
    list_filter = ("start_datetime",)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "created_at")
    search_fields = ("name", "email")

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("code", "event", "price", "status", "customer", "purchased_at")
    list_filter = ("status", "event")
    search_fields = ("code", "event__title", "customer__name")

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "customer", "channel", "status", "created_at", "sent_at")
    list_filter = ("channel", "status")
    search_fields = ("title", "customer__name", "customer__email")
