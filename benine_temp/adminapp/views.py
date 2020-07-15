from authapp.models import ShopUser
from django.shortcuts import get_object_or_404, render
from mainapp.models import Product, ProductCategory
from django.contrib.auth.decorators import user_passes_test

from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from authapp.forms import ShopUserRegistrationForm
from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm, ProductEditForm

from django.views.generic.list import ListView
from django.utils.decorators import method_decorator


def fetch_pages(page, content, offset):
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

    paginator = Paginator(content, offset)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    return pages


class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@user_passes_test(lambda u: u.is_superuser)
def users(request, page=1):
    title = 'Admin:Users'

    users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')

    users_list = fetch_pages(page=page, content=users_list, offset=2)

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
            return HttpResponseRedirect(reverse('admin:users',
                                                args=[1]))
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

        return HttpResponseRedirect(reverse('admin:users',
                                                args=[1]))

    content = {'title': title, 'user_to_delete': user}

    return render(request, 'adminapp/user_delete.html', content)


@user_passes_test(lambda u: u.is_superuser)
def categories(request, page=1):
    title = 'Admin:Categories'

    categories_list = ProductCategory.objects.all()

    categories_list = fetch_pages(page=page, content=categories_list, offset=2)

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
            return HttpResponseRedirect(reverse('admin:categories',
                                                args=[1]))
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
                                                args=[1]))
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

        return HttpResponseRedirect(reverse('admin:categories',
                                                args=[1]))

    content = {'title': title, 'cat_to_delete': category}

    return render(request, 'adminapp/cat_delete.html', content)


@user_passes_test(lambda u: u.is_superuser)
def products(request, pk, page=1):
    title = 'Admin:Products'

    category = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category__pk=pk).order_by('name')

    products_list = fetch_pages(page=page, content=products_list, offset=2)

    content = {
        'title': title,
        'category': category,
        'objects': products_list,
    }

    return render(request, 'adminapp/products.html', content)


def product_create(request, pk):
    title = 'Product:Create'
    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('admin:products', args=[pk, 1]))
    else:
        product_form = ProductEditForm(initial={'category': category})

    content = {'title': title,
               'prod_form': product_form,
               'category': category
               }

    return render(request, 'adminapp/prod_create.html', content)


def product_read(request, pk):
    title = 'Product:Inspect'
    product = get_object_or_404(Product, pk=pk)
    content = {'title': title, 'object': product, }

    return render(request, 'adminapp/product_read.html', content)


def product_update(request, pk):
    title = 'Product:Update'

    edit_product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        edit_form = ProductEditForm(request.POST, request.FILES,
                                    instance=edit_product)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:product_update',
                                                args=[edit_product.pk]))
    else:
        edit_form = ProductEditForm(instance=edit_product)

    content = {'title': title,
               'prod_form': edit_form,
               'category': edit_product.category
               }

    return render(request, 'adminapp/prod_create.html', content)


def product_delete(request, pk):
    title = 'Product:Remove'

    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        return HttpResponseRedirect(reverse('admin:products',
                                            args=[product.category.pk, 1]))

    content = {'title': title, 'prod_to_delete': product}

    return render(request, 'adminapp/prod_delete.html', content)

