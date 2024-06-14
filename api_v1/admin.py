from django.contrib import admin

from .models import City, Street, Address, Contract, RequestTheme, Request, News


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city')
    list_display_links = ('id', 'name', 'city')
    search_fields = ('name', 'city__name')
    list_filter = ('city',)
    ordering = ('city', 'name',)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'street', 'number', 'corpus')
    list_display_links = ('id', 'street', 'number', 'corpus')
    search_fields = ('street__name', 'street__city__name', 'number', 'corpus')
    list_filter = ('street__city', 'street')
    ordering = ('street__city', 'street', 'number')


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'user', 'address')
    list_display_links = ('id', 'number', 'user', 'address')
    search_fields = ('number', 'user__username', 'address__street__name')
    list_filter = ('user', 'address__street__city')
    ordering = ('number',)


@admin.register(RequestTheme)
class RequestThemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    list_display_links = ('id', 'name', 'description')
    search_fields = ('name', 'description')
    ordering = ('name',)


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'theme', 'status')
    list_display_links = ('id', 'user', 'theme', 'status')
    search_fields = ('user__username', 'theme__name', 'request')
    list_filter = ('status', 'theme')
    ordering = ('-status', 'theme')


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'status', 'created_at', 'updated_at')
    list_display_links = ('id', 'title', 'slug', 'status', 'created_at', 'updated_at')
    search_fields = ('title', 'slug', 'content')
    list_filter = ('status', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created_at',)
