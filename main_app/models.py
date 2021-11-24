from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import models


class Client(models.Model):
    first_name = models.CharField('Имя', max_length=50, blank=False)
    last_name = models.CharField('Фамилия', max_length=50, blank=False)
    middle_name = models.CharField('Отчетство', max_length=50, blank=True)
    phone_number = models.CharField('Номер телефона', max_length=20, blank=False)
    email = models.EmailField('Email', blank=True)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.last_name + ' ' + self.first_name


class Request(models.Model):
    preferences = models.TextField('Описание', max_length=200, blank=False)
    client = models.ForeignKey('Client', on_delete=models.CASCADE, verbose_name='Клиент',
                               related_name='requests', null=True)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return 'Заявка №' + str(self.id)


def month_hence():
    return timezone.now() + timezone.timedelta(days=30)


def some_days_hence():
    return timezone.now() + timezone.timedelta(days=7)


class Order(models.Model):
    STATUSES = (
        ('Создан', 'Создан'),
        ('Ожидает подписания договора', 'Ожидает подписания договора'),
        ('Ожидает оплаты', 'Ожидает оплаты'),
        ('Стадия дизайана', 'Стадия дизайана'),
        ('В производстве', 'В производстве'),
        ('Доставляется', 'Доставляется'),
        ('Завершен', 'Завершен'),
        ('Отменен', 'Отменен')
    )
    start_date = models.DateTimeField('Время создания', default=timezone.now)
    end_date = models.DateTimeField('Время окончания', default=month_hence())
    status = models.CharField('Статус', choices=STATUSES, max_length=40, default='Создан')

    request = models.OneToOneField('Request', on_delete=models.SET_NULL, verbose_name='Заявка',
                                   related_name='order', null=True)
    design = models.ForeignKey('Design', on_delete=models.SET_NULL, verbose_name='Дизайн',
                               related_name='order', null=True)
    workers = models.ManyToManyField('Worker', verbose_name='Работники',
                                     related_name='orders', blank=True)

    def clean(self):
        if self.start_date <= self.end_date:
            raise ValidationError('Дата окончания не может быть меньше даты создания')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Заказ №' + str(self.id)


class Design(models.Model):
    start_date = models.DateTimeField('Время создания', default=timezone.now)
    end_date = models.DateTimeField('Время окончания', default=some_days_hence())

    def clean(self):
        if self.start_date <= self.end_date:
            raise ValidationError('Дата окончания не может быть меньше даты создания')

    class Meta:
        verbose_name = 'Дизайн'
        verbose_name_plural = 'Дизайн'

    def __str__(self):
        return 'Дизайн для заказа №' + str(self.order.id)


class Production(models.Model):
    start_date = models.DateTimeField('Время создания', default=timezone.now)
    end_date = models.DateTimeField('Время окончания', default=some_days_hence())

    design = models.OneToOneField('Design', on_delete=models.SET_NULL, verbose_name='Дизайн',
                                  related_name='production', null=True)

    def clean(self):
        if self.start_date <= self.end_date:
            raise ValidationError('Дата окончания не может быть меньше даты создания')

    class Meta:
        verbose_name = 'Производство'
        verbose_name_plural = 'Производство'

    def __str__(self):
        return 'Производство по дизайну №' + str(self.design.id)


class Product(models.Model):
    TYPES = (
        ('Кровать', 'Кровать'),
        ('Диван', 'Диван'),
        ('Кресло', 'Кресло'),
    )
    name = models.CharField('Название', max_length=50, blank=False)
    type = models.CharField('Вид', choices=TYPES, max_length=30, default='Кровать')
    size = models.FloatField('Размер, м3', null=False)
    color = models.CharField('Цвет', max_length=50, blank=False)

    production = models.OneToOneField('Design', on_delete=models.SET_NULL, verbose_name='Производство',
                                      related_name='product', null=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class Worker(models.Model):
    POSITIONS = (
        ('Дизайнер', 'Дизайнер'),
        ('Мастер', 'Мастер'),
        ('Водитель', 'Водитель')
    )
    first_name = models.CharField('Имя', max_length=50, blank=False)
    last_name = models.CharField('Фамилия', max_length=50, blank=False)
    middle_name = models.CharField('Отчетство', max_length=50, blank=True)
    phone_number = models.CharField('Номер телефона', max_length=20, blank=False)
    email = models.EmailField('Email', blank=True)
    position = models.CharField('Должность', choices=POSITIONS, max_length=40, default='Дизайнер')

    class Meta:
        verbose_name = 'Работник'
        verbose_name_plural = 'Работники'

    def __str__(self):
        return self.position + ' | ' + self.last_name + ' ' + self.first_name


class Car(models.Model):
    numbers = models.CharField('Номера', max_length=50, blank=False)
    model = models.CharField('Модель', max_length=50, blank=False)
    color = models.CharField('Цвет', max_length=50, blank=False)
    worker = models.ForeignKey('Worker', on_delete=models.SET_NULL, verbose_name='Работник',
                               related_name='cars', null=True)

    class Meta:
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'

    def __str__(self):
        return self.model + ' ' + self.numbers


class Agreement(models.Model):
    description = models.TextField('Описание', max_length=200, blank=False)
    price = models.IntegerField('Стоимость, руб.')
    order = models.OneToOneField('Order', on_delete=models.SET_NULL, verbose_name='Заказ',
                                 related_name='agreement', null=True)

    def clean(self):
        if self.price <= 0:
            raise ValidationError('Стоимость не может быть менее 1 руб.')

    class Meta:
        verbose_name = 'Договор'
        verbose_name_plural = 'Договоры'

    def __str__(self):
        return 'Договор №' + str(self.id)


class Delivery(models.Model):
    timestamp_start = models.DateTimeField('Время начала', default=timezone.now)
    timestamp_end = models.DateTimeField('Время конца', default=timezone.now)
    description = models.TextField('Описание', max_length=200, blank=False)
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, verbose_name='Заказ',
                              related_name='deliveries', null=True)

    class Meta:
        verbose_name = 'Доставка'
        verbose_name_plural = 'Доставки'

    def __str__(self):
        return 'Доставка №' + str(self.id)

# class Pet(models.Model):
#     TYPES = (('Кошка', 'Кошка'),
#              ('Собака', 'Собака'))
#     name = models.CharField('Кличка', max_length=50, blank=False)
#     type = models.CharField('Вид', choices=TYPES, max_length=30, default='Кошка')
#     weight = models.FloatField('Вес', null=False)
#     breed = models.CharField('Порода', max_length=50, blank=False)
#     recommendations = models.TextField('Рекомендации', max_length=1000, blank=True)
#
#     client = models.ForeignKey('Client', on_delete=models.CASCADE, verbose_name='Клиент',
#                                related_name='pets')
#
#     class Meta:
#         verbose_name = 'Питомец'
#         verbose_name_plural = 'Питомцы'
#
#     def __str__(self):
#         return self.name
#
#
# class Request(models.Model):
#     description = models.TextField('Описание', max_length=200, blank=False)
#     pet = models.ForeignKey('Pet', on_delete=models.SET_NULL, verbose_name='Питомец',
#                             related_name='requests', null=True)
#
#     class Meta:
#         verbose_name = 'Заявка'
#         verbose_name_plural = 'Заявки'
#
#     def __str__(self):
#         return 'Заявка №' + str(self.id)
#
#
# class Order(models.Model):
#     STATUSES = (
#         ('Создан', 'Создан'),
#         ('Ожидает подписания договора', 'Ожидает подписания договора'),
#         ('Ожидает оплаты', 'Ожидает оплаты'),
#         ('В транспортировке (от владельца)', 'В транспортировке (от владельца)'),
#         ('На передержке', 'На передержке'),
#         ('В транспортировке (к владельцу)', 'В транспортировке (к владельцу)'),
#         ('Завершен', 'Завершен'),
#         ('Отменен', 'Отменен')
#     )
#     created_at = models.DateTimeField('Время создания', default=timezone.now)
#     duration = models.IntegerField('Длительность, дни')
#     status = models.CharField('Статус', choices=STATUSES, max_length=40, default='Создан')
#     request = models.OneToOneField('Request', on_delete=models.SET_NULL, verbose_name='Заявка',
#                                    related_name='order', null=True)
#     workers = models.ManyToManyField('Worker', verbose_name='Работники',
#                                      related_name='orders', blank=True)
#
#     def clean(self):
#         if self.duration <= 0:
#             raise ValidationError('Длительность не может быть менее 1 дня')
#
#     class Meta:
#         verbose_name = 'Заказ'
#         verbose_name_plural = 'Заказы'
#
#     def __str__(self):
#         return 'Заказ №' + str(self.id)
#
#
# class Agreement(models.Model):
#     description = models.TextField('Описание', max_length=200, blank=False)
#     price = models.IntegerField('Стоимость, руб.')
#     order = models.OneToOneField('Order', on_delete=models.SET_NULL, verbose_name='Заказ',
#                                  related_name='agreement', null=True)
#
#     def clean(self):
#         if self.price <= 0:
#             raise ValidationError('Стоимость не может быть менее 1 руб.')
#
#     class Meta:
#         verbose_name = 'Договор'
#         verbose_name_plural = 'Договоры'
#
#     def __str__(self):
#         return 'Договор №' + str(self.id)
#
#
# class Worker(models.Model):
#     POSITIONS = (
#         ('Перевозчик', 'Перевозчик'),
#         ('Кипер', 'Кипер')
#     )
#     first_name = models.CharField('Имя', max_length=50, blank=False)
#     last_name = models.CharField('Фамилия', max_length=50, blank=False)
#     middle_name = models.CharField('Отчетство', max_length=50, blank=True)
#     phone_number = models.CharField('Номер телефона', max_length=20, blank=False)
#     email = models.EmailField('Email', blank=True)
#     position = models.CharField('Должность', choices=POSITIONS, max_length=40, default='Кипер')
#
#     class Meta:
#         verbose_name = 'Работник'
#         verbose_name_plural = 'Работники'
#
#     def __str__(self):
#         return self.position + ' | ' + self.last_name + ' ' + self.first_name
#
#
# class Car(models.Model):
#     POSITIONS = (
#         ('Перевозчик', 'Перевозчик'),
#         ('Кипер', 'Кипер')
#     )
#     numbers = models.CharField('Номера', max_length=50)
#     mark_n_model = models.CharField('Марка, модель', max_length=50)
#     color = models.CharField('Цвет', max_length=50, blank=True)
#     worker = models.ForeignKey('Worker', on_delete=models.SET_NULL, verbose_name='Работник',
#                                related_name='cars', null=True)
#
#     class Meta:
#         verbose_name = 'Машина'
#         verbose_name_plural = 'Машины'
#
#     def __str__(self):
#         return self.mark_n_model + ' ' + self.numbers
#
#
# class TransportEvent(models.Model):
#     timestamp_start = models.DateTimeField('Время начала', default=timezone.now)
#     timestamp_end = models.DateTimeField('Время конца', default=timezone.now)
#     description = models.TextField('Описание', max_length=200, blank=False)
#     order = models.ForeignKey('Order', on_delete=models.SET_NULL, verbose_name='Заказ',
#                               related_name='transport_events', null=True)
#
#     class Meta:
#         verbose_name = 'Событие перевозки'
#         verbose_name_plural = 'События перевозки'
#
#     def __str__(self):
#         return 'Перевозка №' + str(self.id)
#
#
# class Report(models.Model):
#     created_at = models.DateTimeField('Время создания', default=timezone.now)
#     description = models.TextField('Описание', max_length=200, blank=False)
#     order = models.ForeignKey('Order', on_delete=models.SET_NULL, verbose_name='Заказ',
#                               related_name='reports', null=True)
#     video = models.FileField('Видеофайл', upload_to='report_videos')
#     image = models.ImageField('Изображение', upload_to='report_images')
#
#     def clean(self):
#         approved_video_extensions = ('.mp4', '.ogv', '.webm', 'webvtt')
#         if not self.video.name.lower().endswith(approved_video_extensions):
#             raise ValidationError(
#                 f"Расширение видеофайла может быть только одим из следующих: {', '.join(approved_video_extensions)}")
#
#     class Meta:
#         verbose_name = 'Отчет'
#         verbose_name_plural = 'Отчеты'
#
#     def __str__(self):
#         return 'Отчет №' + str(self.id)
