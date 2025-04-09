# myproject/users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Payment(models.Model):
    PAYMENT_METHODS = (
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    payment_date = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey('lms.Course', on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    lesson = models.ForeignKey('lms.Lesson', on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)

    def __str__(self):
        return f"Payment by {self.user.username} - {self.amount} ({self.payment_method})"

    class Meta:
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'
