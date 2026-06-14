from django.urls import path, include

app_name = 'Accounts'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('api/v0/', include('Accounts.api.v0.urls')),
]