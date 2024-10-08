from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, AccountMeter

# Customizing the display for the Account model in the admin interface
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    
    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')
    ordering = ('-created_at',)
    

# Register the Account model with the custom admin interface
# admin.site.register(Account, AccountAdmin)

# Customizing the display for the AccountMeter model in the admin interface
class AccountMeterAdmin(admin.ModelAdmin):
    list_display = ('account', 'meter_number', 'v_rating', 'c_rating', 'house_number', 'created_at', 'updated_at')
    search_fields = ('account__first_name', 'account__last_name', 'meter_number', 'house_number')
    ordering = ('meter_number',)
    readonly_fields = ('created_at', 'updated_at')

# Register the AccountMeter model with the custom admin interface
admin.site.register(AccountMeter, AccountMeterAdmin)
