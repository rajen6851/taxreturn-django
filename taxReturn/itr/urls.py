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
]