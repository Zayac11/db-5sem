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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        kwargs["queryset"] = Worker.objects.filter(position__startswith='Водитель')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class DesignAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp_start', 'timestamp_end')
    list_filter = ('type', 'timestamp_start')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'order':
            kwargs["queryset"] = Order.objects.all()
        elif db_field.name == 'worker':
            kwargs["queryset"] = Worker.objects.filter(position__startswith='Дизайнер')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ProductionAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp_start', 'timestamp_end')
    list_filter = ('timestamp_start',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'design':
            kwargs["queryset"] = Design.objects.all()
        elif db_field.name == 'worker':
            kwargs["queryset"] = Worker.objects.filter(position__startswith='Мастер')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'size', 'color')
    search_fields = ('name', 'color')
    list_filter = ('size', 'type')


class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('order', 'timestamp_start', 'timestamp_end', 'description')
    list_filter = ('timestamp_start', 'timestamp_end')

    # def formfield_for_manytomany(self, db_field, request, kwargs):
    #     if db_field.name == 'products':
    #         kwargs["queryset"] = Product.objects.ALL
    #     return super().formfield_for_manytomany(db_field, request, kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'order':
            kwargs["queryset"] = Order.objects.all()
        elif db_field.name == 'worker':
            kwargs["queryset"] = Worker.objects.filter(position__startswith='Водитель')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


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
