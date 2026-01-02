# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User
# from taxReturn.itr.models import ITR
from itr.models import ITR

from django.utils import timezone
from datetime import datetime

from django.contrib.auth.decorators import login_required
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        pan = request.POST.get("pan")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("signup")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.pan_number = pan
        user.role = "USER"
        user.save()

        messages.success(request, "Account created successfully")
        return redirect("login")

    return render(request, "accounts/signup.html")


# def login_view(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)

#             # Role-based redirect
#             if user.role == "ADMIN":
#                 return redirect("/admin-panel/")
#             else:
#                 return redirect("/dashboard/")

#         else:
#             messages.error(request, "Invalid credentials")
#             return redirect("login")

#     return render(request, "accounts/login.html")
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return role_redirect(user)

        messages.error(request, "Invalid credentials")
        return redirect("login")

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")

def role_redirect(user):
    if user.role == "ADMIN":
        return redirect("admin_dashboard")
    return redirect("user_dashboard")

# @login_required
# def personal_details(request):
#     user = request.user
    
#     # Get latest ITR
#     itr = ITR.objects.filter(user=user).order_by('-id').first()
    
#     # If ITR doesn't exist, create one
#     if not itr:
#         itr = ITR.objects.create(
#             user=user,
#             assessment_year='2025-26',
#             status='draft',
#             full_name=user.get_full_name() or user.username
#         )
    
#     if request.method == "POST":
#         try:
#             # Get form data
#             full_name = request.POST.get('full_name', '').strip()
#             email = request.POST.get('email', '').strip()
#             pan = request.POST.get('pan', '').strip().upper()
#             aadhaar = request.POST.get('aadhaar', '').strip()
#             dob = request.POST.get('dob', '').strip()
#             phone = request.POST.get('phone', '').strip()
            
#             # ✅ Update User model
#             if full_name:
#                 # Split full name into first and last name
#                 name_parts = full_name.split(' ', 1)
#                 user.first_name = name_parts[0]
#                 if len(name_parts) > 1:
#                     user.last_name = name_parts[1]
            
#             if email:
#                 user.email = email
            
#             # Update PAN in User model
#             if pan and len(pan) == 10:
#                 # Check if PAN already exists (excluding current user)
#                 existing_user = User.objects.filter(pan_number=pan).exclude(id=user.id).first()
#                 if existing_user:
#                     messages.error(request, f"PAN {pan} is already registered with user {existing_user.username}")
#                 else:
#                     user.pan_number = pan
#             elif pan:
#                 messages.warning(request, "PAN should be exactly 10 characters")
            
#             # Update phone if field exists
#             if hasattr(user, 'phone'):
#                 user.phone = phone
            
#             user.save()
            
#             # ✅ Update ITR model
#             if full_name:
#                 itr.full_name = full_name
            
#             if pan and len(pan) == 10:
#                 itr.pan = pan
            
#             if aadhaar and aadhaar.isdigit() and len(aadhaar) == 12:
#                 itr.aadhaar = aadhaar
#             elif aadhaar:
#                 messages.warning(request, "Aadhaar should be 12 digits")
            
#             if dob:
#                 try:
#                     itr.dob = datetime.strptime(dob, '%Y-%m-%d').date()
#                 except ValueError:
#                     messages.warning(request, "Invalid date format. Please use YYYY-MM-DD")
            
#             itr.save()
            
#             messages.success(request, "Personal details updated successfully!")
#             return redirect('personal_details')
            
#         except Exception as e:
#             messages.error(request, f"Error saving details: {str(e)}")
    
#     # Prepare context with today's date
#     context = {
#         'user': user,
#         'itr': itr,
#         'today': timezone.now().date()  # ✅ This is missing in your current code
#     }
    
#     return render(request, 'User/account/personal_details.html', context)
@login_required
def personal_details(request):
    user = request.user
    
    # Get latest ITR
    itr = ITR.objects.filter(user=user).order_by('-id').first()
    
    # If ITR doesn't exist, create one
    if not itr:
        itr = ITR.objects.create(
            user=user,
            assessment_year='2025-26',
            status='draft',
            # full_name=user.full_name or user.get_full_name() or user.username
        )
    
    if request.method == "POST":
        try:
            # Get form data
            full_name = request.POST.get('full_name', '').strip()
            email = request.POST.get('email', '').strip()
            pan = request.POST.get('pan', '').strip().upper()
            aadhaar = request.POST.get('aadhaar', '').strip()
            dob = request.POST.get('dob', '').strip()
            phone = request.POST.get('phone', '').strip()
            
            # -------------------------
            # Update User model
            # -------------------------
            if full_name:
                user.full_name = full_name
                # Split full name into first and last name
                name_parts = full_name.split(' ', 1)
                user.first_name = name_parts[0]
                user.last_name = name_parts[1] if len(name_parts) > 1 else ''
            
            if email:
                user.email = email
            
            if pan and len(pan) == 10:
                existing_user = User.objects.filter(pan_number=pan).exclude(id=user.id).first()
                if existing_user:
                    messages.error(request, f"PAN {pan} is already registered with user {existing_user.username}")
                else:
                    user.pan_number = pan
            elif pan:
                messages.warning(request, "PAN should be exactly 10 characters")
            
            if aadhaar and aadhaar.isdigit() and len(aadhaar) == 12:
                existing_user = User.objects.filter(aadhaar_number=aadhaar).exclude(id=user.id).first()
                if existing_user:
                    messages.error(request, f"Aadhaar {aadhaar} is already registered with another user")
                else:
                    user.aadhaar_number = aadhaar
            elif aadhaar:
                messages.warning(request, "Aadhaar should be 12 digits")
            
            if dob:
                try:
                    user.dob = datetime.strptime(dob, '%Y-%m-%d').date()
                except ValueError:
                    messages.warning(request, "Invalid date format. Please use YYYY-MM-DD")
            
            if phone:
                user.phone = phone
            
            user.save()
            
            # -------------------------
            # Update ITR model (snapshot)
            # -------------------------
            # itr.full_name = user.full_name
            # itr.pan = user.pan_number
            # itr.aadhaar = user.aadhaar_number
            # itr.dob = user.dob
            # itr.save()
            
            messages.success(request, "Personal details updated successfully!")
            return redirect('personal_details')
        
        except Exception as e:
            messages.error(request, f"Error saving details: {str(e)}")
    
    # Prepare context
    context = {
        'user': user,
        'itr': itr,
        'today': timezone.now().date()
    }
    
    return render(request, 'User/account/personal_details.html', context)
