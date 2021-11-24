from django.contrib.admin import AdminSite
from django.contrib import admin

from .models import *

AdminSite.index_title = 'Администрация сайта'
AdminSite.site_title = 'Производство спальной мебели на заказ'
AdminSite.site_header = 'Производство спальной мебели на заказ'


class ClientAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'phone_number', 'email')


class RequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'preferences')
    list_filter = ('client',)
    search_fields = ('preferences',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'request', 'timestamp_start', 'timestamp_end', 'status')
    list_filter = ('timestamp_start', 'status')


class AgreementAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'description', 'price')


class WorkerAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'phone_number', 'email', 'position')


class CarAdmin(admin.ModelAdmin):
    list_display = ('numbers', 'model', 'color', 'worker')


class DesignAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp_start', 'timestamp_end')
    list_filter = ('type', 'timestamp_start')


class ProductionAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp_start', 'timestamp_end')
    list_filter = ('timestamp_start',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'size', 'color')
    search_fields = ('name', 'color')
    list_filter = ('size', 'type')


class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('order', 'timestamp_start', 'timestamp_end', 'description')
    list_filter = ('timestamp_start', 'timestamp_end')


admin.site.register(Client, ClientAdmin)
admin.site.register(Request, RequestAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Agreement, AgreementAdmin)
admin.site.register(Worker, WorkerAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Design, DesignAdmin)
admin.site.register(Production, ProductionAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Delivery, DeliveryAdmin)
