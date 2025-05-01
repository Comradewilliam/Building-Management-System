from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Sum, Count, Q
from datetime import datetime, timedelta
from .models import Material, Stock, MaterialHistory, Project, UserProfile
from django.db.models import F

import requests

def get_flask_data():
    flask_url = "https://polished-crow-selected.ngrok-free.app/api/data"  # Flask endpoint
    response = requests.get(flask_url)
    if response.status_code == 200:
        return response.json()
    return None

@login_required
def dashboard(request):
    flask_data = get_flask_data()
    total_materials = Material.objects.count()
    available_stock = Stock.objects.aggregate(total=Sum('quantity'))['total'] or 0
    low_stock_items = Stock.objects.filter(
        quantity__lte=F('material__min_quantity')
    ).count()
    today = datetime.now().date()
    today_usage = MaterialHistory.objects.filter(
        type='usage',
        date__date=today
    ).aggregate(total=Sum('quantity'))['total'] or 0
    recent_activities = MaterialHistory.objects.select_related(
        'material', 'user'
    ).order_by('-date')[:10]
    low_stock_alerts = Stock.objects.select_related('material').filter(
        quantity__lte=F('material__min_quantity')
    )
    context = {
        'total_materials': total_materials,
        'available_stock': available_stock,
        'low_stock_items': low_stock_items,
        'today_usage': today_usage,
        'recent_activities': recent_activities,
        'low_stock_alerts': low_stock_alerts,
        'flask_data': flask_data,  # <-- Add this line
    }
    return render(request, 'dashboard.html', context)

@login_required
def view_stock(request):
    stock_items = Stock.objects.select_related('material').all()
    return render(request, 'view_stock.html', {'stock_items': stock_items})

@login_required
def register_arrival(request):
    if request.method == 'POST':
        material_id = request.POST.get('material')
        quantity = float(request.POST.get('quantity'))
        date = request.POST.get('date')
        supplier = request.POST.get('supplier')
        notes = request.POST.get('notes')
        material = get_object_or_404(Material, id=material_id)
        stock, created = Stock.objects.get_or_create(material=material)
        stock.quantity += quantity
        stock.save()
        MaterialHistory.objects.create(
            material=material,
            type='arrival',
            quantity=quantity,
            date=date,
            user=request.user,
            notes=notes,
            supplier=supplier
        )
        messages.success(request, 'Material arrival registered successfully!')
        return redirect('view_stock')
    materials = Material.objects.all()
    recent_arrivals = MaterialHistory.objects.filter(
        type='arrival'
    ).select_related('material').order_by('-date')[:5]
    return render(request, 'register_arrival.html', {
        'materials': materials,
        'recent_arrivals': recent_arrivals
    })

@login_required
def register_usage(request):
    if request.method == 'POST':
        material_id = request.POST.get('material')
        quantity = float(request.POST.get('quantity'))
        date = request.POST.get('date')
        project_id = request.POST.get('project')
        location = request.POST.get('location')
        notes = request.POST.get('notes')
        material = get_object_or_404(Material, id=material_id)
        project = get_object_or_404(Project, id=project_id)
        stock = get_object_or_404(Stock, material=material)
        if stock.quantity < quantity:
            messages.error(request, 'Insufficient stock available!')
            return redirect('register_usage')
        stock.quantity -= quantity
        stock.save()
        MaterialHistory.objects.create(
            material=material,
            type='usage',
            quantity=quantity,
            date=date,
            user=request.user,
            notes=notes,
            project=project,
            location=location
        )
        messages.success(request, 'Material usage registered successfully!')
        return redirect('view_stock')
    materials = Material.objects.all()
    projects = Project.objects.all()
    recent_usage = MaterialHistory.objects.filter(
        type='usage'
    ).select_related('material', 'project').order_by('-date')[:5]
    return render(request, 'register_usage.html', {
        'materials': materials,
        'projects': projects,
        'recent_usage': recent_usage
    })

@login_required
def edit_stock(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    if request.method == 'POST':
        quantity = float(request.POST.get('quantity'))
        stock.quantity = quantity
        stock.save()
        messages.success(request, 'Stock updated successfully!')
        return redirect('view_stock')
    return render(request, 'edit_stock.html', {'stock': stock})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    return render(request, 'profile.html', {'profile': profile})

@login_required
def settings(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        request.user.email = request.POST.get('email')
        request.user.save()
        profile.phone = request.POST.get('phone')
        profile.notifications = request.POST.get('notifications') == 'on'
        profile.save()
        messages.success(request, 'Settings updated successfully!')
        return redirect('settings')
    return render(request, 'settings.html', {'profile': profile})