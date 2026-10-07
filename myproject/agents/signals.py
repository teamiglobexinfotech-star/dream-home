from django.db.models.signals import post_save
from django.dispatch import receiver
from properties.models import Property, Enquiry
from customers.models import Notification

# Jab admin kisi agent ko lead assign kare (ya enquiry create ho aur agent sath me ho)
# @receiver(post_save, sender=Enquiry)
# def notify_agent_on_lead_assignment(sender, instance, created, **kwargs):
#     if instance.agent:
#         # User type ensure karne ke liye (agar agent custom model hai toh .user lagayein)
#         agent_user = getattr(instance.agent, 'user', instance.agent)

#         # Check karein ki yeh notification pehle se toh nahi bani hai
#         notification_exists = Notification.objects.filter(
#             user=agent_user,
#             title="New Lead Assigned",
#             message=f"A new lead ({instance.name}) has been assigned to you."
#         ).exists()

#         if not notification_exists:
#             Notification.objects.create(
#                 user=agent_user,
#                 title="New Lead Assigned",
#                 message=f"A new lead ({instance.name}) has been assigned to you."
#             )

# Jab agent property add kare
@receiver(post_save, sender=Property)
def notify_agent_on_property_status(sender, instance, created, **kwargs):
    if instance and hasattr(instance, 'agent') and instance.agent:
        agent_user = getattr(instance.agent, 'user', instance.agent)
        if created:
            Notification.objects.create(
                user=agent_user,
                title="New Property Listed",
                message=f"Your property '{instance.title}' has been listed successfully."
            )