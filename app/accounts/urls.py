
from django.urls import path, include
from .views import login_view, user_register_view, user_info_view,\
    logout_view, user_comments_view, MyLoginView, get_users_list,\
    UserUpdateView
from .api import user_change_password, user_info, user_register

app_name = 'accounts'
urlpatterns = [
    path('login/', MyLoginView.as_view(), name='login_view'),
    path('register/', user_register_view, name='register_view'),
    path('profile/', UserUpdateView.as_view(), name='user_info_view'),
    path('profile/comments', user_comments_view, name='user_comments_view'),
    path('logout/', logout_view, name='user_logout_view'),
    path('users-list/', get_users_list, name='users_list'),
    path('api/change-password/', user_change_password, name='api-password-change'),
    path('api/user-info/', user_info, name='api-user-info'),
    path('api/register/', user_register, name='api-register'),
]
