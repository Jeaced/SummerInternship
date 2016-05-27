from django.contrib import admin
from .models import Item, Component, Composition, Order, OrderContent

# Register your models here.

class ItemAdmin(admin.ModelAdmin):
	list_display = ('title', 'created', 'units', 'price_per_unit')
	list_filter = ('title', 'created', 'price_per_unit')
	search_fields = ('title',)
	date_hierarchy = 'created'
	ordering = ['title', '-created']

class ComponentAdmin(admin.ModelAdmin):
	list_display = ('title', 'created', 'units', 'price_per_unit')
	list_filter = ('title', 'created', 'price_per_unit')
	search_fields = ('title',)
	date_hierarchy = 'created'
	ordering = ['title', '-created']	

class CompositionAdmin(admin.ModelAdmin):
	list_display = ('item', 'component', 'amount')
	list_filter = ('item', 'component')
	search_fields = ('item__title', 'component__title')
	oredring = ['item.id']	

admin.site.register(Item, ItemAdmin)
admin.site.register(Component, ComponentAdmin)
admin.site.register(Composition, CompositionAdmin)