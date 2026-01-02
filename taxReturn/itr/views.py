# # itr/views.py
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.utils import timezone
# from datetime import datetime
# from .models import ITR
# from .forms import ITRForm

# # @login_required
# # def start_itr(request):
# #     """Create new ITR draft"""
# #     year = datetime.now().year
# #     ay = f"{year}-{year+1}"
    
# #     # Check if draft already exists
# #     existing_draft = ITR.objects.filter(
# #         user=request.user, 
# #         status='draft'
# #     ).first()
    
# #     if existing_draft:
# #         return redirect('itr_detail', itr_id=existing_draft.id)
    
# #     # Create new ITR
# #     itr = ITR.objects.create(
# #         user=request.user,
# #         assessment_year=ay,
# #         status='draft'
# #     )
    
# #     return redirect('itr_detail', itr_id=itr.id)

# # @login_required
# # def itr_detail(request, itr_id):
# #     # Get ITR for the logged-in user
# #     itr = get_object_or_404(ITR, id=itr_id, user=request.user)

# #     if request.method == 'POST':
# #         # Include request.FILES for file uploads
# #         form = ITRForm(request.POST, request.FILES, instance=itr)
# #         if form.is_valid():
# #             form.save()

# #             # Mark ITR as submitted if user clicked Submit
# #             if 'submit_itr' in request.POST:
# #                 itr.status = 'submitted'
# #                 itr.save()

# #             return redirect('itr_detail', itr_id=itr.id)
# #     else:
# #         form = ITRForm(instance=itr)

# #     return render(request, 'User/ITR/detail.html', {
# #         'itr': itr,
# #         'form': form
# #     })

# @login_required
# def start_itr(request):
#     """Create new ITR draft"""
#     year = datetime.now().year
#     ay = f"{year}-{year+1}"
    
#     # Check if draft already exists
#     existing_draft = ITR.objects.filter(
#         user=request.user, 
#         status='draft'
#     ).first()
    
#     if existing_draft:
#         return redirect('itr_detail', itr_id=existing_draft.id)
    
#     # Create new ITR with minimal data
#     itr = ITR.objects.create(
#         user=request.user,
#         assessment_year=ay,
#         status='draft'
#     )
    
#     return redirect('itr_detail', itr_id=itr.id)

# @login_required
# def itr_detail(request, itr_id):
#     # Get ITR for the logged-in user
#     itr = get_object_or_404(ITR, id=itr_id, user=request.user)
    
#     if request.method == 'POST':
#         # Include request.FILES for file uploads
#         form = ITRForm(request.POST, request.FILES, instance=itr, request=request)  # ✅ Yeh line important hai
#         if form.is_valid():
#             form.save()

#             # Mark ITR as submitted if user clicked Submit
#             if 'submit_itr' in request.POST:
#                 itr.status = 'submitted'
#                 itr.save()

#             return redirect('itr_detail', itr_id=itr.id)
#     else:
#         # Pass request to form for auto-fill
#         form = ITRForm(instance=itr, request=request)  # ✅ Yeh line important hai

#     return render(request, 'User/ITR/detail.html', {
#         'itr': itr,
#         'form': form,
#         'user': request.user  # Pass user to template for display
#     })


# @login_required
# def itr_list(request):
#     """List all ITRs for user"""
#     itrs = ITR.objects.filter(user=request.user).order_by('-created_at')
#     return render(request, 'User/ITR/list.html', {'itrs': itrs})

# @login_required
# def update_status(request, itr_id):
#     """Update ITR status (e.g., submit)"""
#     if request.method == 'POST':
#         itr = get_object_or_404(ITR, id=itr_id, user=request.user)
#         new_status = request.POST.get('status')
        
#         if new_status in dict(ITR.STATUS_CHOICES):
#             itr.status = new_status
#             itr.save()
        
#         return redirect('itr_detail', itr_id=itr.id)
    
# @login_required
# def itr_view(request, id):
#     itr = ITR.objects.get(id=id, user=request.user)

#     return render(request, 'User/ITR/view.html', {
#         'itr': itr
#     })
# itr/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime
from .models import ITR
from .forms import ITRForm

@login_required
def start_itr(request):
    """Create new ITR draft"""
    year = datetime.now().year
    ay = f"{year}-{year+1}"
    
    # Check if a draft already exists
    existing_draft = ITR.objects.filter(user=request.user, status='draft').first()
    if existing_draft:
        return redirect('itr_detail', itr_id=existing_draft.id)
    
    # Create new ITR with minimal data
    itr = ITR.objects.create(
        user=request.user,
        assessment_year=ay,
        status='draft'
    )
    
    return redirect('itr_detail', itr_id=itr.id)


@login_required
def itr_detail(request, itr_id):
    """View & edit a single ITR"""
    itr = get_object_or_404(ITR, id=itr_id, user=request.user)
    
    if request.method == 'POST':
        # Include request.FILES for file uploads
        form = ITRForm(request.POST, request.FILES, instance=itr, request=request)
        if form.is_valid():
            form.save()

            # Mark ITR as submitted if user clicked "Submit"
            if 'submit_itr' in request.POST:
                itr.status = 'submitted'
                itr.save()

            return redirect('itr_detail', itr_id=itr.id)
    else:
        # Pass request to form for auto-fill (User fields + ITR fields)
        form = ITRForm(instance=itr, request=request)

    return render(request, 'User/ITR/detail.html', {
        'itr': itr,
        'form': form,
        'user': request.user,  # For template display
        'today': timezone.now().date()  # For max date in DOB input
    })


@login_required
def itr_list(request):
    """List all ITRs for the logged-in user"""
    itrs = ITR.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'User/ITR/list.html', {'itrs': itrs})


@login_required
def update_status(request, itr_id):
    """Update ITR status (e.g., submit)"""
    if request.method == 'POST':
        itr = get_object_or_404(ITR, id=itr_id, user=request.user)
        new_status = request.POST.get('status')
        
        if new_status in dict(ITR.STATUS_CHOICES):
            itr.status = new_status
            itr.save()
        
        return redirect('itr_detail', itr_id=itr.id)


@login_required
def itr_view(request, id):
    """View ITR in read-only mode"""
    itr = get_object_or_404(ITR, id=id, user=request.user)
    return render(request, 'User/ITR/view.html', {
        'itr': itr
    })
