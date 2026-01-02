from django.urls import path
from . import views

urlpatterns = [
    path('api/chat/', views.chat_api, name='chat_api'),
    path('health/', views.health_check, name='health_check'),
    path('test-page/', views.test_page, name='test_page'),
    path('test/', views.test_api, name='test_api'),  # Custom test POST
    path('calculator/', views.tax_calculator, name='tax_calculator'),
]
