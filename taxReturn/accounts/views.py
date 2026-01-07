from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.utils import timezone

from .models import User
from itr.models import ITR


def signup_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        pan = request.POST.get("pan")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("signup")

        user = User.objects.create_user(
            email=email,
            password=password
        )
        user.pan_number = pan
        user.role = "USER"
        user.save()

        messages.success(request, "Account created successfully")
        return redirect("login")

    return render(request, "accounts/signup.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)
            return role_redirect(user)

        messages.error(request, "Invalid email or password")
        return redirect("login")

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")

def logingoogle(request):
    return render(request, "auth/login.html")



def role_redirect(user):
    if user.role == "ADMIN":
        return redirect("admin_dashboard")
    return redirect("user_dashboard")


@login_required
def personal_details(request):
    user = request.user

    itr = ITR.objects.filter(user=user).order_by('-id').first()
    if not itr:
        itr = ITR.objects.create(
            user=user,
            assessment_year='2025-26',
            status='draft'
        )

    if request.method == "POST":
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        pan = request.POST.get('pan', '').strip().upper()
        aadhaar = request.POST.get('aadhaar', '').strip()
        dob = request.POST.get('dob', '').strip()
        phone = request.POST.get('phone', '').strip()

        if full_name:
            user.full_name = full_name
            parts = full_name.split(' ', 1)
            user.first_name = parts[0]
            user.last_name = parts[1] if len(parts) > 1 else ''

        if email:
            user.email = email

        if pan and len(pan) == 10:
            if not User.objects.filter(pan_number=pan).exclude(id=user.id).exists():
                user.pan_number = pan

        if aadhaar and aadhaar.isdigit() and len(aadhaar) == 12:
            if not User.objects.filter(aadhaar_number=aadhaar).exclude(id=user.id).exists():
                user.aadhaar_number = aadhaar

        if dob:
            user.dob = datetime.strptime(dob, '%Y-%m-%d').date()

        if phone:
            user.phone = phone

        user.save()
        messages.success(request, "Details updated successfully")
        return redirect("personal_details")

    return render(request, "User/account/personal_details.html", {
        "user": user,
        "itr": itr,
        "today": timezone.now().date()
    })
