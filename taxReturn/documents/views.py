from django.shortcuts import render
from itr.models import ITR
from django.contrib.auth.decorators import login_required
# def my_documents(request):
#     docs = ITR.objects.filter(user=request.user, status='draft').last()
#     return render(request, 'User/Documents/my_documents.html', {'docs': docs})
@login_required
def my_documents(request):
    docs = ITR.objects.filter(
        user=request.user,
        status='submitted'
    ).order_by('-created_at').first()

    return render(request, 'User/Documents/my_documents.html', {'docs': docs})

