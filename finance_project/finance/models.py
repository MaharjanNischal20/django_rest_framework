from django.contrib.auth.models import User
from django.db import models

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    sender = models.ForeignKey(Customer, related_name='sent_transactions', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Customer, related_name='received_transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=[('send', 'Send'), ('receive', 'Receive')])
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.transaction_type == 'send':
            self.sender.balance -= self.amount
            self.receiver.balance += self.amount
        elif self.transaction_type == 'receive':
            self.sender.balance += self.amount
            self.receiver.balance -= self.amount
        self.sender.save()
        self.receiver.save()
        super().save(*args, **kwargs)
