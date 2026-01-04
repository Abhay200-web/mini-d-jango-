from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record
import os


def home(request):
    records = Record.objects.all()

    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )

        if user:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
        else:
            messages.success(request, "Invalid Login Credentials")

        return redirect('home')

    return render(request, 'home.html', {'records': records})


def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out")
    return redirect('home')


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


def customer_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': record})
    messages.success(request, "Login Required")
    return redirect('home')


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


def update_record(request, pk):
    if not request.user.is_authenticated:
        messages.success(request, "Login Required")
        return redirect('home')

    record = Record.objects.get(id=pk)
    old_image = record.image

    form = AddRecordForm(request.POST or None, request.FILES or None, instance=record)
    if form.is_valid():
        if 'image' in request.FILES and old_image.name != 'records/default.png':
            if os.path.isfile(old_image.path):
                os.remove(old_image.path)

        form.save()
        messages.success(request, "Record Updated Successfully")
        return redirect('home')

    return render(request, 'update_record.html', {'form': form})


def delete_record(request, pk):
    if not request.user.is_authenticated:
        messages.success(request, "Login Required")
        return redirect('home')

    record = Record.objects.get(id=pk)
    if record.image and record.image.name != 'records/default.png':
        if os.path.isfile(record.image.path):
            os.remove(record.image.path)

    record.delete()
    messages.success(request, "Record Deleted Successfully")
    return redirect('home')
