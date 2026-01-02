from django.urls import path
from .views import my_documents

urlpatterns = [
    path('my-documents/', my_documents, name='my_documents'),
]

