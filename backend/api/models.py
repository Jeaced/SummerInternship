from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

UNITS_CHOICES = (
		('g', 'gramms'),
		('mg', 'milligramms'),
		('kg', 'kilogramms'),
		('pc', 'pieces'),
		('l', 'liter'),
		('ml', 'milliliter')
		)

PAYMENT_CHOICES = (
		('cash', 'cash'),
		('cc', 'credit card'),
		('cheque', 'cheque')
		)

class Item(models.Model):
	title = models.CharField(max_length=100, blank=False)
	image_link = models.TextField(default='', blank=True)
	created = models.DateField(auto_now_add=True)
	units = models.CharField(max_length=2, choices=UNITS_CHOICES, default='pc')
	price_per_unit = models.DecimalField(max_digits=12, decimal_places=2)

	class Meta:
		ordering = ['title', '-created']

	def __str__(self):
		return self.title

class Component(models.Model):
	title = models.CharField(max_length=120, blank=False)
	created = models.DateField(auto_now_add=True)
	units = models.CharField(max_length=2, choices=UNITS_CHOICES, default='g')
	price_per_unit = models.DecimalField(max_digits=12, decimal_places=2)

	class Meta:
		ordering = ['title', '-created']

	def __str__(self):
		return self.title

class Composition(models.Model):
	item = models.ForeignKey(Item, on_delete=models.CASCADE)	
	component = models.ForeignKey(Component, on_delete=models.CASCADE)
	amount = models.IntegerField(blank=False)

class Order(models.Model):
    date = models.DateField(default=datetime.date.today)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    payment_method = models.CharField(max_length=6, choices=PAYMENT_CHOICES, default='cc')
    user = models.ForeignKey(User, related_name='orders', 
                             on_delete=models.SET_NULL, 
                             null=True)
    items = models.ManyToManyField(Item)

    class Meta:
        ordering = ['-date']

        def __str__(self):
       	    return str(self.id)	

class ItemHistory(models.Model):
	date = models.DateField()
	item = models.ForeignKey(Item, on_delete=models.CASCADE, unique_for_date="date")
	amount = models.IntegerField(blank=False)

	class Meta:
		ordering = ['-date']

class ComponentHistory(models.Model):
	date = models.DateField()
	component = models.ForeignKey(Component, on_delete=models.CASCADE, unique_for_date="date")
	amount = models.IntegerField(blank=False)

	class Meta:
		ordering = ['-date']			
