# views.py
from django.shortcuts import render, get_object_or_404
from ..models import User, Category
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from admin_app.Forms.categories.Forms import CategoryForm
from custom_decorators.admin.decorators import staff_required,ensure_platform_configured
from admin_app.services import AppConfig


@staff_required
@ensure_platform_configured 
def categories_list(request):
    request.session['page'] = 'Admin Categories'
    user_with_brand = AppConfig.Ownership.get_owner()
    site_name = user_with_brand.brand_name if user_with_brand else None
    site_logo = user_with_brand.brand_image_url if user_with_brand else None
    staff_count = User.objects.filter(is_staff=True, is_active=True).count()
    categories = Category.objects.all()
    page_number = request.GET.get('page', 1)
    paginator = Paginator(categories, 10)  # Show 5 categories per page
    page_obj = paginator.get_page(page_number)

    context = {
        "categories": page_obj,
        "site_name":site_name,
        "site_logo":site_logo
    }
    
    return render(request, 'admin_app/partials/list_elements/categories_list.html', context)
    

@staff_required
@ensure_platform_configured 
def categories(request):
    request.session['page'] = 'Admin Categories'
    staff_count = User.objects.filter(is_staff=True, is_active=True).count()
    user_with_brand = AppConfig.Ownership.get_owner()
    site_name = user_with_brand.brand_name if user_with_brand else None
    site_logo = user_with_brand.brand_image_url if user_with_brand else None
    context={
        "site_name":site_name,
        "site_logo":site_logo
    }
    return render(request, 'admin_app/pages/categories/categories.html',context)


@staff_required
@ensure_platform_configured 
def add_category(request):
    user_with_brand = AppConfig.Ownership.get_owner()
    site_name = user_with_brand.brand_name if user_with_brand else None
    site_logo = user_with_brand.brand_image_url if user_with_brand else None
    if request.method == 'POST':
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponse(status=204, headers={'HX-Trigger': 'category_list_update'})
            # 204, empty response 
    else:
        form = CategoryForm()

    return render(request, 'admin_app/partials/form_elements/categories/category_form.html', {
        'form': form,
        "site_name":site_name,
        "site_logo":site_logo})


@staff_required
@ensure_platform_configured 
def edit_category(request, category_id):
    user_with_brand = AppConfig.Ownership.get_owner()
    site_name = user_with_brand.brand_name if user_with_brand else None
    site_logo = user_with_brand.brand_image_url if user_with_brand else None
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'category_list_update'})

    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'admin_app/partials/form_elements/categories/category_form.html', {
        'form': form,
        "site_name":site_name,
        "site_logo":site_logo
        })


@staff_required
@ensure_platform_configured 
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return JsonResponse({'message': 'Category deleted successfully'})
