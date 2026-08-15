from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

# Create your models here.
class Tenant(TenantMixin):
    class Status(models.TextChoices):
        TRIAL = 'trial', 'Trial'
        ACTIVE = 'active', 'Active'
        SUSPENDED = 'suspended', 'Suspended'
        CANCELLED = 'cancelled', 'Cancelled'

    name = models.CharField(max_length=155)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.TRIAL)

    is_active = models.BooleanField(default=True)
    is_trial = models.BooleanField(default=True)
    is_paid_plan = models.BooleanField(default=False)
    paid_until = models.DateField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    auto_create_schema = True

class Domain(DomainMixin):
    pass
    