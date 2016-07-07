from django.contrib import admin

from database.models import LaundryShop, Price, Service, UserProfile, Transaction, Order, Fees


class PricesInline(admin.TabularInline):
    model = Price


class LaundryShopAdmin(admin.ModelAdmin):
    inlines = [PricesInline]


admin.site.register(LaundryShop, LaundryShopAdmin)
admin.site.register(Service)
admin.site.register(UserProfile)
admin.site.register(Transaction)
admin.site.register(Order)
admin.site.register(Fees)
