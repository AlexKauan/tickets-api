from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import EventViewSet, CustomerViewSet, TicketViewSet, NotificationViewSet

router = DefaultRouter()
router.register(r"events", EventViewSet, basename="event")
router.register(r"customers", CustomerViewSet, basename="customer")
router.register(r"tickets", TicketViewSet, basename="ticket")
router.register(r"notifications", NotificationViewSet, basename="notification")

urlpatterns = [
    path("", include(router.urls)),
]
