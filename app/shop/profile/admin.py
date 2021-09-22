from django.contrib import admin

from profile.models import User, Position, Company


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    pass


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

