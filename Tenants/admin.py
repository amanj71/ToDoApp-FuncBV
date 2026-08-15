from django.contrib import admin
from django_tenants.admin import TenantAdminMixin

from .models import Tenant, Domain

# Register your models here.
class TenantAdimn(TenantAdminMixin, admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_on']

class DomainAdmin(TenantAdminMixin, admin.ModelAdmin):
    pass

admin.site.register(Tenant, TenantAdimn)
admin.site.register(Domain, DomainAdmin)