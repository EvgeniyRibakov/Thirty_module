from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


@shared_task
def deactivate_inactive_users():
    threshold = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=threshold, is_active=True)
    count = 0
    for user in inactive_users:
        user.is_active = False
        user.save()
        count += 1
    return f"Deactivated {count} inactive users"
