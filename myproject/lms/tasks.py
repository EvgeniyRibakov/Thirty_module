from celery import shared_task
from django.core.mail import send_mail
from .models import Course, Subscription
from django.conf import settings


@shared_task
def send_course_update_email(course_id):
    course = Course.objects.get(id=course_id)
    subscriptions = Subscription.objects.filter(course=course)
    recipients = [subscription.user.email for subscription in subscriptions if subscription.user.email]

    if recipients:
        subject = f"Course Updated: {course.title}"
        message = f"The course '{course.title}' has been updated. Check out the new content!"
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipients,
            fail_silently=False,
        )
    return f"Sent update email for course {course_id} to {len(recipients)} users"
