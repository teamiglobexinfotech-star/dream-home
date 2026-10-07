from django.db.models.signals import post_save
from django.dispatch import receiver
from properties.models import Property, Enquiry
from customers.models import Notification

@receiver(post_save, sender=Property)
def create_property_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            title="New Property Added",
            message=f"Property '{instance.title}' has been listed."
        )

@receiver(post_save, sender=Enquiry)
def create_enquiry_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            title="New Enquiry Received",
            message=f"New enquiry from {instance.name}."
        )
        