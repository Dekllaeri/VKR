from django.contrib import admin
from .models import City, Street, Address, Contract, RequestTheme, Request, News


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')
    search_fields = ('name', 'city__name')
    list_filter = ('city',)
    ordering = ('city', 'name',)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('street', 'number', 'corpus')
    search_fields = ('street__name', 'street__city__name', 'number', 'corpus')
    list_filter = ('street__city', 'street')
    ordering = ('street__city', 'street', 'number')


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('number', 'user', 'address')
    search_fields = ('number', 'user__username', 'address__street__name')
    list_filter = ('user', 'address__street__city')
    ordering = ('number',)


@admin.register(RequestTheme)
class RequestThemeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    ordering = ('name',)


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'theme', 'status')
    search_fields = ('user__username', 'theme__name', 'request')
    list_filter = ('status', 'theme')
    ordering = ('-status', 'theme')


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status', 'created_at', 'updated_at')
    search_fields = ('title', 'slug', 'content')
    list_filter = ('status', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created_at',)

    # def save_model(self, request, obj, form, change):
    #     if not obj.slug or not change:
    #         obj.slug = slugify(obj.title)
    #     super().save_model(request, obj, form, change)