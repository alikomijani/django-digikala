from django.shortcuts import render, redirect
from django.urls import reverse
from accounts.forms import UserLoginForm, UserRegisterFrom, MyAuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from products.models import Comment
# Create your views here.


class MyLoginView(LoginView):
    template_name = 'accounts/login_view.html'
    authentication_form = MyAuthenticationForm


def login_view(request):
    if request.method == 'GET':
        form = AuthenticationForm()
    else:

        form = AuthenticationForm(data=request.POST, request=request)
        if form.is_valid():
            login(request=request, user=form.get_user())
            next = request.GET.get('next', reverse('accounts:user_info_view'))
            return redirect(next)
    context = {
        "form": form,
        "next": request.GET.get('next', reverse('accounts:user_info_view'))
    }
    return render(request, 'accounts/login_view.html', context)


def user_register_view(request):
    status = 200
    if request.method == 'GET':
        form = UserRegisterFrom()
    else:
        form = UserRegisterFrom(request.POST,)
        if form.is_valid():
            user = form.save(commit=True)
            login(request=request, user=user)
            return redirect('accounts:user_info_view')
        else:
            status = 400
    context = {
        "form": form
    }
    return render(request, 'accounts/register_view.html', context, status=status)


@login_required()
def user_info_view(request):
    return render(request, 'accounts/user_info.html', {
        "user": request.user
    })


def logout_view(request):
    logout(request)
    return redirect('accounts:user_info_view')


@login_required()
def user_comments_view(request):
    query = Comment.objects.filter(user=request.user)
    return render(request, 'accounts/user_comments.html', {
        'comments': query
    })
