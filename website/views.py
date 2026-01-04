from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .forms import SignUpForm, AddRecordForm
from .models import Record
import os


# HOME (LOGIN + SEARCH + FILTER + PAGINATION)

def home(request):
    records = Record.objects.all().order_by('-created_at')

    # SEARCH & FILTER
    search_query = request.GET.get('search', '')
    city_filter = request.GET.get('city', '')
    state_filter = request.GET.get('state', '')

    if search_query:
        records = records.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query)
        )

    if city_filter:
        records = records.filter(city__icontains=city_filter)

    if state_filter:
        records = records.filter(state__icontains=state_filter)

    # PAGINATION
    paginator = Paginator(records, 5)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # LOGIN LOGIC
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )

        if user:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
        else:
            messages.success(request, "Invalid Login Credentials")

        return redirect('home')

    return render(request, 'home.html', {
        'records': page_obj,   
        'page_obj': page_obj,
        'search_query': search_query,
        'city_filter': city_filter,
        'state_filter': state_filter,
    })



# LOGOUT

def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out")
    return redirect('home')



# REGISTER

def register_user(request):
    form = SignUpForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1']
        )
        login(request, user)
        messages.success(request, "Registration Successful")
        return redirect('home')

    return render(request, 'register.html', {'form': form})



# VIEW SINGLE RECORD

def customer_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': record})

    messages.success(request, "Login Required")
    return redirect('home')



# ADD RECORD

def add_record(request):
    if not request.user.is_authenticated:
        messages.success(request, "Login Required")
        return redirect('home')

    form = AddRecordForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Record Added Successfully")
        return redirect('home')

    return render(request, 'add_record.html', {'form': form})



# UPDATE RECORD

def update_record(request, pk):
    if not request.user.is_authenticated:
        messages.success(request, "Login Required")
        return redirect('home')

    record = Record.objects.get(id=pk)
    old_image = record.image

    form = AddRecordForm(request.POST or None, request.FILES or None, instance=record)

    if form.is_valid():
        # delete old image if replaced
        if 'image' in request.FILES and old_image and old_image.name != 'records/default.png':
            if os.path.isfile(old_image.path):
                os.remove(old_image.path)

        form.save()
        messages.success(request, "Record Updated Successfully")
        return redirect('home')

    return render(request, 'update_record.html', {'form': form})



# DELETE RECORD

def delete_record(request, pk):
    if not request.user.is_authenticated:
        messages.success(request, "Login Required")
        return redirect('home')

    record = Record.objects.get(id=pk)

    # delete image file
    if record.image and record.image.name != 'records/default.png':
        if os.path.isfile(record.image.path):
            os.remove(record.image.path)

    record.delete()
    messages.success(request, "Record Deleted Successfully")
    return redirect('home')
