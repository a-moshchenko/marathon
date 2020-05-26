from django.contrib import admin
from .models import SubCategory, Category, Enterprise, PhoneNumber
from django.utils.safestring import mark_safe


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Enterprise)
class EnterpriseAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_image', 'description', 'city', 'adress', 'number')

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" ')

    get_image.short_description = 'логотип'

    def number(self, obj):
        return obj.phone.number
    number.admin_order_field = 'number'


admin.site.register(PhoneNumber)
