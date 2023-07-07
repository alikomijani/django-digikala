
from django.urls import path
from .views import login_view, user_register_view, user_info_view,\
    logout_view, user_comments_view, MyLoginView, get_users_list, UserUpdateView


app_name = 'accounts'
urlpatterns = [
    path('login/', MyLoginView.as_view(), name='login_view'),
    path('register/', user_register_view, name='register_view'),
    path('profile/', UserUpdateView.as_view(), name='user_info_view'),
    path('profile/comments', user_comments_view, name='user_comments_view'),
    path('logout/', logout_view, name='user_logout_view'),
    path('users-list/', get_users_list, name='users_list'),
]
