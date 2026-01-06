# itr/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.start_itr, name='start_itr'),
    path('list/', views.itr_list, name='itr_list'),
    # urls.py
path('itr/view/<int:id>/', views.itr_view, name='itr_view'),

    path('detail/<int:itr_id>/', views.itr_detail, name='itr_detail'),
    path('update-status/<int:itr_id>/', views.update_status, name='update_status'),

    # Admin URLs
    path('admin-panel/itr-list/', views.admin_itr_list, name='admin_itr_list'),
    path('admin/itr/details/<int:itr_id>/', views.itr_details_page, name='itr_details_page'),
    
    # PDF URLs
    path('admin/itr/view-pdf/<int:itr_id>/', views.view_itr_pdf, name='view_itr_pdf'),
    path('admin/itr/download-pdf/<int:itr_id>/', views.download_itr_pdf, name='download_itr_pdf'),
    
]