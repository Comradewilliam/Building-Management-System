from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Material(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    unit = models.CharField(max_length=20)
    min_quantity = models.FloatField(default=0)  # Add this field
    
    def __str__(self):
        return self.name

class Stock(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.material.name} - {self.quantity} {self.material.unit}"

class Project(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class MaterialHistory(models.Model):
    TYPE_CHOICES = (
        ('arrival', 'Arrival'),
        ('usage', 'Usage'),
    )
    
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='history')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    quantity = models.FloatField()
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = models.TextField(blank=True, null=True)
    supplier = models.CharField(max_length=100, blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return f"{self.material.name} - {self.type} - {self.quantity}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    notifications = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.username