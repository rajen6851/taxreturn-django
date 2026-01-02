# taxApp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('dashboard/', views.dashboard_home, name='dashboard'),

    path('tax-center/', views.tax_center, name='tax_center'),

    path('itr/start/', views.itr_start, name='itr_start'),
    path('itr/income/', views.itr_income, name='itr_income'),
    path('itr/deductions/', views.itr_deductions, name='itr_deductions'),
    path('itr/bank/', views.itr_bank, name='itr_bank'),
    path('itr/summary/', views.itr_summary, name='itr_summary'),
    path('itr/submit/', views.itr_submit, name='itr_submit'),
    path('tax_planning/', views.tax_planning, name='tax_planning'),
    path('ai_tax_plan/', views.ai_tax_plan, name='ai_tax_plan'),
    path('tax_savings/', views.tax_savings, name='tax_savings'),
    path('documents/', views.document_cloud, name='documents'),
    path('orders/', views.my_orders, name='orders'),
path('notifications/', views.notifications, name='notifications'),
 path('messages/', views.messages, name='messages'),   
 path('profile/', views.profile, name='profile'),   

      # Dashboard / Core
    path('tax-center/', views.tax_center, name='tax_center'),
    path('investments/', views.investments, name='investments'),
    path('notices/', views.notices, name='notices'),
    path('gst-solutions/', views.gst_solutions, name='gst_solutions'),
    path('my-details/', views.my_details, name='my_details'),
    path('document-cloud/', views.document_cloud, name='document_cloud'),
    path('calculator/', views.calculator, name='calculator'),

    # Account Section
    path('subscription/', views.subscription, name='subscription'),
    path('pricing/', views.pricing, name='pricing'),
    path('blogs/', views.blogs, name='blogs'),
    path('settings/', views.settings_page, name='settings'),
    path('help/', views.help_support, name='help'),

    # Footer pages
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    path('service-terms/', views.service_terms, name='service_terms'),


]
