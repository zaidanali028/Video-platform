# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from ..models import User, Category
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from admin_app.Forms.categories.Forms import CategoryForm

@login_required(login_url='admin_login')
def categories_list(request):
    request.session['page'] = 'Admin Categories'
    staff_count = User.objects.filter(is_staff=True, is_active=True).count()
    if staff_count < 2:
        return redirect('config_platform')

    categories = Category.objects.all()
    page_number = request.GET.get('page', 1)
    paginator = Paginator(categories, 10)  # Show 5 categories per page
    page_obj = paginator.get_page(page_number)

    context = {
        "categories": page_obj
    }
    
    return render(request, 'admin_app/partials/list_elements/categories_list.html', context)
    

@login_required(login_url='admin_login')
def categories(request):
    request.session['page'] = 'Admin Categories'
    staff_count = User.objects.filter(is_staff=True, is_active=True).count()
    if staff_count < 2:
        return redirect('config_platform')
    return render(request, 'admin_app/pages/categories/categories.html')

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'category_list_update'})
        # 204, empty response 

    else:
        form = CategoryForm()

    return render(request, 'admin_app/partials/form_elements/categories/category_form.html', {'form': form})

def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'category_list_update'})

    else:
        form = CategoryForm(instance=category)
    return render(request, 'admin_app/partials/form_elements/categories/category_form.html', {'form': form})

def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return JsonResponse({'message': 'Category deleted successfully'})
