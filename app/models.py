from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime as dt


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    payment_status = models.CharField(max_length=10, blank=True, null=True)
    is_premium = models.BooleanField(default=False)
    location = models.CharField(max_length=60, blank=True)
    phone_number = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} Profile"

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Plan(models.Model):
    """Represents either a Plan or OnceOff payment type"""

    name = models.CharField(max_length=50, unique=True)
    amount = models.IntegerField()
    interval = models.CharField(
        max_length=11,
        blank=True,
        null=True,
        help_text="Payment frequency. Only required if this is a subscription plan.",
    )
    duration = models.IntegerField()
    currency = models.CharField(max_length=3, default="USD")
    created_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Plan"
        verbose_name_plural = "Plans"

    def __str__(self):
        return self.name
