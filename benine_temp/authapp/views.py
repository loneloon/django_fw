from django.shortcuts import render
from authapp.forms import ShopUserLoginForm

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
        'title': 'Authentication',
        'form': form,
    }
    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:index'))