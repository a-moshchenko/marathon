from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class SubCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, blank=True,
                                 verbose_name='Категория')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class PhoneNumber(models.Model):
    number = models.CharField(max_length=13, verbose_name='номер телефона')


class Enterprise(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    image = models.ImageField(upload_to='enterprises', null=True, blank=True)
    description = models.TextField(verbose_name='Описание')
    city = models.CharField(max_length=30, verbose_name='Город')
    adress = models.CharField(max_length=100, verbose_name='Адрес')
    phone = models.ForeignKey(PhoneNumber, on_delete=models.CASCADE,
                              verbose_name='номер')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 verbose_name='категория', null=True,
                                 blank=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL,
                                     verbose_name='подкатегория', null=True,
                                     blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Предприятие'
        verbose_name_plural = 'Предприятия'
