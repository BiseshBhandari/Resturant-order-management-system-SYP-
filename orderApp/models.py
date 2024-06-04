from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    product_ID = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='media/', height_field=None, width_field=None, max_length=None)
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    description = models.TextField()
    
    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.first_name}'s cart"


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.first_name}"