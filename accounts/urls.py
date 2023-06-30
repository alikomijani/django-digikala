
from django.urls import path
from .views import login_view
app_name = 'accounts'
urlpatterns = [
    path('login/', login_view, name='login_view')
]
