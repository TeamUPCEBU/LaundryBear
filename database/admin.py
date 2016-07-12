from django.contrib import admin

from database.models import LaundryShop, Service, UserProfile, Transaction, Order, Fees


admin.site.register(LaundryShop)
admin.site.register(Service)
admin.site.register(UserProfile)
admin.site.register(Transaction)
admin.site.register(Order)
admin.site.register(Fees)
