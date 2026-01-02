# from django import forms
# from .models import ITR


# class ITRForm(forms.ModelForm):

#     class Meta:
#         model = ITR
#         fields = [
#             'assessment_year',

#             # Income
#             'salary_income',
#             'business_income',
#             'other_income',

#             # Deductions
#             'deduction_80c',
#             'deduction_80d',

#             # Documents
#             'pan_card',
#             'aadhaar_card',
#             'form_16',
#             'bank_statement',
#         ]

#     def __init__(self, *args, **kwargs):
#         self.request = kwargs.pop('request', None)
#         super().__init__(*args, **kwargs)

#         # Styling
#         for field_name, field in self.fields.items():
#             if field_name in ['pan_card', 'aadhaar_card', 'form_16', 'bank_statement']:
#                 field.widget.attrs.update({'class': 'form-control-file'})
#             else:
#                 field.widget.attrs.update({
#                     'class': 'form-control',
#                     'placeholder': f'Enter {field.label.lower()}'
#                 })

#         # ✅ Auto-fill previous ITR data
#         if self.request and self.request.user.is_authenticated:
#             self.auto_fill_from_previous_itr()

#     def auto_fill_from_previous_itr(self):
#         user = self.request.user

#         previous_itr = ITR.objects.filter(
#             user=user
#         ).exclude(
#             status='draft'
#         ).order_by('-created_at').first()

#         if previous_itr:
#             self.initial.setdefault('salary_income', previous_itr.salary_income)
#             self.initial.setdefault('business_income', previous_itr.business_income)
#             self.initial.setdefault('other_income', previous_itr.other_income)
#             self.initial.setdefault('deduction_80c', previous_itr.deduction_80c)
#             self.initial.setdefault('deduction_80d', previous_itr.deduction_80d)


# # class ITRForm(forms.ModelForm):

# #     class Meta:
# #         model = ITR
# #         fields = [
# #             'full_name',
# #             'pan',
# #             'aadhaar',
# #             'dob',
# #             'salary_income',
# #             'business_income',
# #             'other_income',
# #             'deduction_80c',
# #             'deduction_80d',
# #             'pan_card',
# #             'aadhaar_card',
# #             'form_16',
# #             'bank_statement'
# #         ]
# #         widgets = {
# #             'dob': forms.DateInput(attrs={
# #                 'type': 'date',
# #                 'class': 'form-control'
# #             }),
# #         }

# #     def __init__(self, *args, **kwargs):
# #         self.request = kwargs.pop('request', None)
# #         super().__init__(*args, **kwargs)

# #         # Styling
# #         for field_name, field in self.fields.items():
# #             if field_name in ['pan_card', 'aadhaar_card', 'form_16', 'bank_statement']:
# #                 field.widget.attrs.update({'class': 'form-control-file'})
# #             else:
# #                 field.widget.attrs.update({
# #                     'class': 'form-control',
# #                     'placeholder': f'Enter {field.label.lower()}'
# #                 })

# #         # ✅ Auto fill call
# #         if self.request and self.request.user.is_authenticated:
# #             self.auto_fill_data()

# #     # ✅ MUST BE INSIDE CLASS
# #     def auto_fill_data(self):
# #         user = self.request.user

# #         # ---- USER DATA ----
# #         if not self.initial.get('full_name'):
# #             self.initial['full_name'] = user.get_full_name()

# #         if not self.initial.get('pan') and hasattr(user, 'pan_number'):
# #             self.initial['pan'] = user.pan_number

# #         # ---- PREVIOUS ITR DATA ----
# #         if self.instance and self.instance.pk and self.instance.status == 'draft':
# #             previous_itr = ITR.objects.filter(
# #                 user=user
# #             ).exclude(id=self.instance.id).exclude(
# #                 status='draft'
# #             ).order_by('-created_at').first()

# #             if previous_itr:
# #                 self.initial.setdefault('aadhaar', previous_itr.aadhaar)
# #                 self.initial.setdefault('dob', previous_itr.dob)
# #                 self.initial.setdefault('salary_income', previous_itr.salary_income)
# #                 self.initial.setdefault('business_income', previous_itr.business_income)
# #                 self.initial.setdefault('other_income', previous_itr.other_income)
# #                 self.initial.setdefault('deduction_80c', previous_itr.deduction_80c)
# #                 self.initial.setdefault('deduction_80d', previous_itr.deduction_80d)


from django import forms
from .models import ITR
from accounts.models import User
from datetime import datetime

class ITRForm(forms.ModelForm):
    # Add User fields explicitly
    full_name = forms.CharField(required=False, label='Full Name')
    pan = forms.CharField(required=False, label='PAN Number', max_length=10)
    aadhaar = forms.CharField(required=False, label='Aadhaar Number', max_length=12)
    dob = forms.DateField(required=False, label='Date of Birth', widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = ITR
        fields = [
            'full_name', 'pan', 'aadhaar', 'dob',  # User fields
            'salary_income', 'business_income', 'other_income',
            'deduction_80c', 'deduction_80d',
            'pan_card', 'aadhaar_card', 'form_16', 'bank_statement',
            
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        # Bootstrap styling
        for field_name, field in self.fields.items():
            if field_name in ['pan_card', 'aadhaar_card', 'form_16', 'bank_statement']:
                field.widget.attrs.update({'class': 'form-control-file'})
            else:
                field.widget.attrs.update({'class': 'form-control', 'placeholder': f'Enter {field.label.lower()}'})

        # Auto-fill previous ITR or User data
        if self.request and self.request.user.is_authenticated:
            self.auto_fill_data()

    def auto_fill_data(self):
        user = self.request.user

        # --- Fill User fields ---
        self.initial.setdefault('full_name', user.full_name or f"{user.first_name} {user.last_name}".strip())
        self.initial.setdefault('pan', getattr(user, 'pan_number', ''))
        self.initial.setdefault('aadhaar', getattr(user, 'aadhaar_number', ''))
        self.initial.setdefault('dob', getattr(user, 'dob', None))

        # --- Fill previous ITR fields ---
        if self.instance and self.instance.pk and self.instance.status == 'draft':
            previous_itr = ITR.objects.filter(user=user).exclude(id=self.instance.id).exclude(status='draft').order_by('-created_at').first()
            if previous_itr:
                for field in ['salary_income', 'business_income', 'other_income', 'deduction_80c', 'deduction_80d']:
                    self.initial.setdefault(field, getattr(previous_itr, field))

    # def save(self, commit=True):
    #     # Save ITR instance
    #     itr = super().save(commit=False)

    #     # Update User model
    #     user = self.request.user
    #     full_name = self.cleaned_data.get('full_name')
    #     if full_name:
    #         parts = full_name.strip().split(' ', 1)
    #         user.first_name = parts[0]
    #         user.last_name = parts[1] if len(parts) > 1 else ''
    #         user.full_name = full_name.strip()

    #     pan = self.cleaned_data.get('pan')
    #     if pan:
    #         user.pan_number = pan.strip().upper()

    #     aadhaar = self.cleaned_data.get('aadhaar')
    #     if aadhaar:
    #         user.aadhaar_number = aadhaar.strip()

    #     dob = self.cleaned_data.get('dob')
    #     if dob:
    #         user.dob = dob

    #     user.save()
    #     if commit:
    #         itr.save()
    #     return itr

    def save(self, commit=True):
        itr = super().save(commit=False)

        # ---------- USER UPDATE ----------
        user = self.request.user

        full_name = self.cleaned_data.get('full_name')
        if full_name:
            parts = full_name.strip().split(' ', 1)
            user.first_name = parts[0]
            user.last_name = parts[1] if len(parts) > 1 else ''
            user.full_name = full_name.strip()

        pan = self.cleaned_data.get('pan')
        if pan:
            user.pan_number = pan.strip().upper()

        aadhaar = self.cleaned_data.get('aadhaar')
        if aadhaar:
            user.aadhaar_number = aadhaar.strip()

        dob = self.cleaned_data.get('dob')
        if dob:
            user.dob = dob

        user.save()

        # ---------- CALCULATE SUMMARY (BACKEND TRUST) ----------
        from .utils import calculate_itr_summary
        itr = calculate_itr_summary(itr)

        if commit:
            itr.save()

        return itr

