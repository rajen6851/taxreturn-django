from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'taxApp/home.html')

@login_required
def dashboard_home(request):
    return render(request, 'taxApp/dashboard.html')

@login_required
def tax_center(request):
    return render(request, 'taxApp/tax_center.html')

@login_required
def itr_start(request):
    return render(request, 'taxApp/itr_start.html')

@login_required
def itr_income(request):
    return render(request, 'taxApp/itr_income.html')

@login_required
def itr_deductions(request):
    return render(request, 'taxApp/itr_deductions.html')

@login_required
def itr_bank(request):
    return render(request, 'taxApp/itr_bank.html')

@login_required
def itr_summary(request):
    return render(request, 'taxApp/itr_summary.html')

@login_required
def itr_submit(request):
    return render(request, 'taxApp/itr_submit.html')

@login_required
def document_cloud(request):
    return render(request, 'taxApp/documents.html')

@login_required
def my_orders(request):
    return render(request, 'taxApp/orders.html')

@login_required
def tax_planning(request):
    return render(request, 'taxApp/orders.html')


@login_required
def tax_planning(request):
    return render(request, 'taxApp/orders.html')


@login_required
def ai_tax_plan(request):
    return render(request, 'taxApp/orders.html')


@login_required
def tax_savings(request):
    return render(request, 'taxApp/orders.html')


@login_required
def tax_center(request):
    return render(request, 'pages/tax_center.html')

@login_required
def investments(request):
    return render(request, 'pages/investments.html')

@login_required
def notices(request):
    return render(request, 'pages/notices.html')

@login_required
def gst_solutions(request):
    return render(request, 'pages/gst_solutions.html')

@login_required
def my_details(request):
    return render(request, 'pages/my_details.html')

@login_required
def document_cloud(request):
    return render(request, 'pages/document_cloud.html')

@login_required
def calculator(request):
    return render(request, 'pages/calculator.html')


# Account
@login_required
def subscription(request):
    return render(request, 'pages/subscription.html')

def pricing(request):
    return render(request, 'pages/pricing.html')

def blogs(request):
    return render(request, 'pages/blogs.html')

@login_required
def settings_page(request):
    return render(request, 'pages/settings.html')

def help_support(request):
    return render(request, 'pages/help.html')


# Footer
def terms(request):
    return render(request, 'pages/terms.html')

def privacy(request):
    return render(request, 'pages/privacy.html')

def service_terms(request):
    return render(request, 'pages/service_terms.html')


def notifications(request):
    return render(request, 'pages/service_terms.html')


def notifications(request):
    return render(request, 'pages/service_terms.html')

def messages(request):
    return render(request, 'pages/service_terms.html')



def profile(request):
    return render(request, 'pages/service_terms.html')
