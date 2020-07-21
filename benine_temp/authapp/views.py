from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authapp.forms import ShopUserLoginForm
from authapp.forms import ShopUserRegistrationForm
from authapp.forms import ShopUserEditForm

from authapp.models import ShopUser


def login(request):
    if request.method == 'POST':
        form = ShopUserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                # return HttpResponseRedirect('/')
                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = ShopUserLoginForm()
    # form = ShopUserLoginForm()
    context = {
        'title': 'Sign In',
        'form': form,
    }
    return render(request, 'authapp/login.html', context)


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:index'))


def register(request):
    title = 'Registration'

    if request.method == 'POST':
        register_form = ShopUserRegistrationForm(request.POST, request.FILES)

        if register_form.is_valid():
            user = register_form.save()
            if user.send_verify_mail():
                print('Verification mail sent!')
        else:
            print('Mail was not sent. Error.')
        return HttpResponseRedirect(reverse('auth:login'))

    else:
        register_form = ShopUserRegistrationForm()

    content = {'title': title, 'register_form': register_form}

    return render(request, 'authapp/register.html', content)


@login_required
def edit(request):
    title = 'Profile Edit'

    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)

    content = {'title': title,
               'edit_form': edit_form}

    return render(request, 'authapp/edit.html', content)


def verify(request, email, activation_key):
    try:
        user = ShopUser.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user)
            return render(request, 'authapp/verification.html')
        else:
            print(f'user verification error: {user}')
            return render(request, 'authapp/verification.html')
    except Exception as e:
        print(f'user verification error: {e.args}')
        return HttpResponseRedirect(reverse('main'))