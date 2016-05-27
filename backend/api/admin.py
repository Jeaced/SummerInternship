from django.contrib import admin
from .models import Item, Component, Composition, Order, OrderContent, ItemHistory, ComponentHistory

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

class OrderAdmin(admin.ModelAdmin):
	list_display = ('date', 'id', 'total_price', 'payment_method', 'user', 'get_content')
	readonly_fields = ('date', 'id', 'total_price', 'payment_method', 'user', 'get_content')
	list_filter = ('date', 'total_price', 'payment_method')
	date_hierarchy = 'date'
	ordering = ['-id']

	def get_content(self, obj):
		order_contents = obj.ordercontent_set.all()
		items = list()
		for oc in order_contents:
			items.append((oc.item.title, oc.amount))	
		return items

	get_content.short_description = 'Items'		

class ItemHistoryAdmin(admin.ModelAdmin):
	list_display = ('date', 'item', 'amount')
	search_fields = ('item__title',)
	readonly_fields = ('date', 'item', 'amount')
	date_hierarchy = 'date'
	oredring = ['-date']	

class ComponentHistoryAdmin(admin.ModelAdmin):
	list_display = ('date', 'component', 'amount')
	search_fields = ('component__title',)
	readonly_fields = ('date', 'component', 'amount')
	date_hierarchy = 'date'
	oredring = ['-date']

admin.site.register(Item, ItemAdmin)
admin.site.register(Component, ComponentAdmin)
admin.site.register(Composition, CompositionAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ItemHistory, ItemHistoryAdmin)
admin.site.register(ComponentHistory, ComponentHistoryAdmin)