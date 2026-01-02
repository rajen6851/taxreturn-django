from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

@login_required
def admin_dashboard(request):
    if request.user.role != "ADMIN":
        return redirect("user_dashboard")
    return render(request, "Admin/admin_dashboard.html")

@login_required
def user_dashboard(request):
    if request.user.role != "USER":
        return redirect("admin_dashboard")
    return render(request, "User/user_dashboard.html")
