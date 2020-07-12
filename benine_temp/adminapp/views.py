from authapp.models import ShopUser
from django.shortcuts import get_object_or_404, render
from mainapp.models import Product, ProductCategory
from django.contrib.auth.decorators import user_passes_test

from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from authapp.forms import ShopUserRegistrationForm
from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    title = 'Admin:Users'

    users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')

    content = {
        'title': title,
        'objects': users_list
    }

    return render(request, 'adminapp/users.html', content)


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    title = 'Users:Create'

    if request.method == 'POST':
        user_form = ShopUserRegistrationForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin:users'))
    else:
        user_form = ShopUserRegistrationForm()

    content = {'title': title, 'update_form': user_form}

    return render(request, 'adminapp/user_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    title = 'Users:Update'

    edit_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        edit_form = ShopUserAdminEditForm(request.POST, request.FILES,
                                          instance=edit_user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:user_update',
                                                args=[edit_user.pk]))
    else:
        edit_form = ShopUserAdminEditForm(instance=edit_user)

    content = {'title': title, 'update_form': edit_form}

    return render(request, 'adminapp/user_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    title = 'Users:Remove'

    user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        user.delete()

        return HttpResponseRedirect(reverse('admin:users'))

    content = {'title': title, 'user_to_delete': user}

    return render(request, 'adminapp/user_delete.html', content)


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    title = 'Admin:Categories'

    categories_list = ProductCategory.objects.all()

    content = {
        'title': title,
        'objects': categories_list
    }

    return render(request, 'adminapp/categories.html', content)


@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    title = 'Category:Create'

    if request.method == 'POST':
        cat_form = ProductCategoryEditForm(request.POST, request.FILES)
        if cat_form.is_valid():
            cat_form.save()
            return HttpResponseRedirect(reverse('admin:categories'))
    else:
        cat_form = ProductCategoryEditForm()

    content = {'title': title, 'cat_form': cat_form}

    return render(request, 'adminapp/cat_create.html', content)


@user_passes_test(lambda u: u.is_superuser)
def category_update(request, pk):
    title = 'Category:Update'

    edit_cat = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        edit_form = ProductCategoryEditForm(request.POST, request.FILES,
                                          instance=edit_cat)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:categories',
                                                args=[edit_cat.pk]))
    else:
        edit_form = ProductCategoryEditForm(instance=edit_cat)

    content = {'title': title, 'cat_form': edit_form}

    return render(request, 'adminapp/cat_create.html', content)


@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    title = 'Category:Remove'

    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        category.delete()

        return HttpResponseRedirect(reverse('admin:categories'))

    content = {'title': title, 'cat_to_delete': category}

    return render(request, 'adminapp/cat_delete.html', content)


@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    title = 'Admin:Products'

    category = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category__pk=pk).order_by('name')

    content = {
        'title': title,
        'category': category,
        'objects': products_list,
    }

    return render(request, 'adminapp/products.html', content)


def product_create(request, pk):
    pass


def product_read(request, pk):
    pass


def product_update(request, pk):
    pass


def product_delete(request, pk):
    pass

