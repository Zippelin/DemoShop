from django.contrib import admin

from product.models import Product

from assortment.models import Assortment


class AssortmentInline(admin.TabularInline):
    model = Assortment
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        AssortmentInline
    ]
