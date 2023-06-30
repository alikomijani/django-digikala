
from django.urls import path
from .views import login_view, user_register_view, user_info_view, logout_view
app_name = 'accounts'
urlpatterns = [
    path('login/', login_view, name='login_view'),
    path('register/', user_register_view, name='register_view'),
    path('profile/', user_info_view, name='user_info_view'),
    path('logout/', logout_view, name='user_logout_view'),
]
