from django.urls import path, include

app_name = 'user'

urlpatterns = [
    path('api/', include('fashionMall.apps.user.api.urls'))
]