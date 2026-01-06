
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime
from .models import ITR
from .forms import ITRForm

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from django.shortcuts import render, get_object_or_404, redirect
import os
from io import BytesIO
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from PIL import Image as PILImage

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

@login_required
def itr_details_page(request, itr_id):
    """View ITR details in HTML page (not PDF)"""
    itr = get_object_or_404(ITR.objects.select_related('user'), id=itr_id)
    
    # Get user information
    user = itr.user
    
    # Get documents information
    document_mappings = [
        ("PAN Document", ["pan_doc", "pan_card"], "PAN Card"),
        ("Aadhaar Document", ["aadhaar_doc", "aadhaar_card"], "Aadhaar Card"),
        ("Form 16", ["form16_doc", "form_16"], "Form 16"),
        ("Bank Statement", ["bank_doc", "bank_statement"], "Bank Statement"),
    ]
    
    documents = []
    for doc_name, possible_fields, icon in document_mappings:
        doc_info = {
            'name': doc_name,
            'icon': icon,
            'found': False,
            'filename': '',
            'url': '',
            'size': '',
            'upload_date': itr.created_at.strftime('%d %b %Y')
        }
        
        for field in possible_fields:
            if hasattr(itr, field):
                doc = getattr(itr, field)
                if doc:
                    doc_info['found'] = True
                    doc_info['filename'] = os.path.basename(str(doc))
                    if hasattr(doc, 'url'):
                        doc_info['url'] = doc.url
                    
                    # Get file size if possible
                    if hasattr(doc, 'size'):
                        doc_info['size'] = f"{doc.size / 1024:.1f} KB"
                    elif hasattr(doc, 'path') and os.path.exists(doc.path):
                        file_size = os.path.getsize(doc.path)
                        doc_info['size'] = f"{file_size / 1024:.1f} KB"
                    
                    break
        
        documents.append(doc_info)
    
    # Calculate financial summary
    try:
        total_income = float(itr.salary_income) + float(itr.business_income) + float(itr.other_income)
        total_deductions = float(itr.deduction_80c) + float(itr.deduction_80d)
        taxable_income = total_income - total_deductions
        
        # Simple tax calculation (you can implement your own tax logic)
        tax_payable = calculate_tax(taxable_income)
    except:
        total_income = 0
        total_deductions = 0
        taxable_income = 0
        tax_payable = 0
    
    # Status badge colors
    status_colors = {
        'draft': 'warning',
        'submitted': 'info',
        'verified': 'success',
        'paid': 'primary'
    }
    
    context = {
        'itr': itr,
        'user': user,
        'documents': documents,
        'total_income': total_income,
        'total_deductions': total_deductions,
        'taxable_income': taxable_income,
        'tax_payable': tax_payable,
        'status_color': status_colors.get(itr.status, 'secondary'),
        'today': timezone.now().date(),
    }
    
    return render(request, 'Admin/itr/itr_details_page.html', context)

def calculate_tax(taxable_income):
    """Simple tax calculation based on Indian tax slabs"""
    tax = 0
    
    if taxable_income <= 250000:
        tax = 0
    elif taxable_income <= 500000:
        tax = (taxable_income - 250000) * 0.05
    elif taxable_income <= 1000000:
        tax = 12500 + (taxable_income - 500000) * 0.20
    else:
        tax = 112500 + (taxable_income - 1000000) * 0.30
    
    # Add 4% health and education cess
    tax = tax + (tax * 0.04)
    
    return tax

def generate_pdf_content(itr):
    """Common function to generate PDF content for both view and download"""
    # Check document fields
    document_mappings = [
        ("PAN Document", ["pan_doc", "pan_card"]),
        ("Aadhaar Document", ["aadhaar_doc", "aadhaar_card"]),
        ("Form 16", ["form16_doc", "form_16"]),
        ("Bank Statement", ["bank_doc", "bank_statement"]),
    ]
    
    found_documents = []
    
    for doc_name, possible_fields in document_mappings:
        doc_value = None
        actual_field = None
        
        for field in possible_fields:
            if hasattr(itr, field):
                value = getattr(itr, field)
                if value and str(value).strip():
                    doc_value = value
                    actual_field = field
                    break
        
        if doc_value:
            filename = os.path.basename(str(doc_value))
            found_documents.append((doc_name, filename, actual_field))
    
    # Create PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []
    
    # Title
    title_style = styles['Heading1']
    title_style.alignment = 1
    title = Paragraph(f"TaxBuddy ITR Report - #{itr.id}", title_style)
    elements.append(title)
    
    # Generation info
    gen_info = Paragraph(f"Generated on: {timezone.now().strftime('%d %b %Y %H:%M:%S')}", styles['Normal'])
    elements.append(gen_info)
    elements.append(Spacer(1, 20))
    
    # User Information
    user = itr.user
    user_header = Paragraph("User Information", styles['Heading2'])
    elements.append(user_header)
    
    user_data = []
    user_data.append(["User ID:", str(user.id)])
    
    if hasattr(user, 'get_full_name') and callable(user.get_full_name):
        full_name = user.get_full_name() or user.username or user.email or "N/A"
    else:
        full_name = getattr(user, 'first_name', '') + " " + getattr(user, 'last_name', '')
        full_name = full_name.strip() or user.username or user.email or "N/A"
    user_data.append(["Name:", full_name])
    
    user_data.append(["Email:", user.email or "N/A"])
    user_data.append(["Username:", user.username or "N/A"])
    
    user_table = Table(user_data, colWidths=[2*inch, 3*inch])
    user_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(user_table)
    elements.append(Spacer(1, 20))
    
    # ITR Information
    itr_header = Paragraph("ITR Details", styles['Heading2'])
    elements.append(itr_header)
    
    itr_data = []
    itr_data.append(["ITR ID:", str(itr.id)])
    itr_data.append(["Assessment Year:", itr.assessment_year])
    itr_data.append(["Status:", getattr(itr, 'get_status_display', lambda: itr.status)()])
    itr_data.append(["Created Date:", itr.created_at.strftime('%d %b %Y %H:%M')])
    
    itr_table = Table(itr_data, colWidths=[2*inch, 3*inch])
    itr_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(itr_table)
    elements.append(Spacer(1, 20))
    
    # Financial Information
    financial_header = Paragraph("Financial Information", styles['Heading2'])
    elements.append(financial_header)
    
    financial_data = [["Description", "Amount (₹)"]]
    
    financial_fields = [
        ("Salary Income", "salary_income"),
        ("Business Income", "business_income"),
        ("Other Income", "other_income"),
        ("Total Income", "total_income"),
        ("Deduction 80C", "deduction_80c"),
        ("Deduction 80D", "deduction_80d"),
        ("Gross Income", "gross_income"),
        ("Total Deduction", "total_deduction"),
        ("Taxable Income", "taxable_income"),
        ("Tax Payable", "tax_payable"),
    ]
    
    for label, field_name in financial_fields:
        try:
            if hasattr(itr, field_name):
                value = getattr(itr, field_name)
                if callable(value):
                    value = value()
                
                try:
                    if value is None:
                        numeric_value = 0.00
                    else:
                        numeric_value = float(value)
                    formatted_value = f"{numeric_value:,.2f}"
                except (ValueError, TypeError):
                    formatted_value = "0.00"
                
                financial_data.append([label, formatted_value])
            else:
                financial_data.append([label, "0.00"])
        except Exception as e:
            financial_data.append([label, "0.00"])
    
    financial_table = Table(financial_data, colWidths=[3*inch, 2*inch])
    financial_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgreen),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(financial_table)
    elements.append(Spacer(1, 20))
    
    # Documents Section
    documents_header = Paragraph("Uploaded Documents", styles['Heading2'])
    elements.append(documents_header)
    
    if found_documents:
        documents_data = [["Document Type", "File Name"]]
        
        for doc_name, filename, field_name in found_documents:
            documents_data.append([doc_name, filename])
        
        documents_table = Table(documents_data, colWidths=[2.5*inch, 2.5*inch])
        documents_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(documents_table)
    else:
        no_docs = Paragraph("No documents uploaded", styles['Normal'])
        elements.append(no_docs)
    
    # Build PDF
    doc.build(elements)
    
    # Get PDF content
    pdf = buffer.getvalue()
    buffer.close()
    
    return pdf


@login_required
def view_itr_pdf(request, itr_id):
    """View PDF in browser (not download)"""
    try:
        itr = get_object_or_404(ITR.objects.select_related('user'), id=itr_id)
        print(f"\nDEBUG: Viewing PDF for ITR #{itr.id}")
        
        # Generate PDF content
        pdf = generate_pdf_content(itr)
        
        # Return for VIEWING
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="TaxBuddy_ITR_Report_{itr.id}.pdf"'
        return response
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"ERROR in view_itr_pdf: {str(e)}")
        error_msg = f"Error generating PDF: {str(e)}\n\nDetails:\n{error_details}"
        return HttpResponse(error_msg, content_type='text/plain')


@login_required

@login_required
def admin_itr_list(request):
    status = request.GET.get('status')

    # Get all ITRs with user information
    itrs = ITR.objects.select_related('user').all().order_by('-created_at')

    if status:
        itrs = itrs.filter(status=status)

    # Add user data to each ITR for easy access
    for itr in itrs:
        itr.user_name = itr.user.get_full_name() or itr.user.username or itr.user.email
        itr.user_initials = (itr.user.first_name or itr.user.email or 'U')[0].upper()

    return render(request, 'Admin/itr/admin_itr_list.html', {
        'itrs': itrs,
        'total': ITR.objects.count(),
        'draft_count': ITR.objects.filter(status='draft').count(),
        'submitted_count': ITR.objects.filter(status='submitted').count(),
    })

def download_itr_pdf(request, itr_id):
    """Download PDF (force download)"""
    try:
        itr = get_object_or_404(ITR.objects.select_related('user'), id=itr_id)
        print(f"\nDEBUG: Downloading PDF for ITR #{itr.id}")
        
        # Generate PDF content (same as view)
        pdf = generate_pdf_content(itr)
        
        # Return for DOWNLOAD
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="TaxBuddy_ITR_Report_{itr.id}.pdf"'
        return response
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"ERROR in download_itr_pdf: {str(e)}")
        error_msg = f"Error generating PDF: {str(e)}\n\nDetails:\n{error_details}"
        return HttpResponse(error_msg, content_type='text/plain')

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
