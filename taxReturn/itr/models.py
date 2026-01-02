from django.db import models
from django.conf import settings
# class ITR(models.Model):
#     STATUS_CHOICES = (
#         ('draft', 'Draft'),
#         ('submitted', 'Submitted'),
#         ('verified', 'Verified'),
#         ('paid', 'Tax Paid'),
#     )

#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     assessment_year = models.CharField(max_length=9)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
#     created_at = models.DateTimeField(auto_now_add=True)

#     # STEP 1 – Personal Info
#     full_name = models.CharField(max_length=200, blank=True)
#     pan = models.CharField(max_length=10, blank=True)
#     aadhaar = models.CharField(max_length=12, blank=True)
#     dob = models.DateField(null=True, blank=True)

#     # STEP 2 – Income
#     salary_income = models.FloatField(default=0)
#     business_income = models.FloatField(default=0)
#     other_income = models.FloatField(default=0)

#     # STEP 3 – Deductions
#     deduction_80c = models.FloatField(default=0)
#     deduction_80d = models.FloatField(default=0)


#     pan_card = models.FileField(upload_to='itr_documents/pan/', null=True, blank=True)
#     aadhaar_card = models.FileField(upload_to='itr_documents/aadhaar/', null=True, blank=True)
#     form_16 = models.FileField(upload_to='itr_documents/form16/', null=True, blank=True)
#     bank_statement = models.FileField(upload_to='itr_documents/bank/', null=True, blank=True)

#     def total_income(self):
#         return self.salary_income + self.business_income + self.other_income
# from django.db import models
# from django.conf import settings

class ITR(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('verified', 'Verified'),
        ('paid', 'Tax Paid'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='itrs'
    )

    assessment_year = models.CharField(max_length=9)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)

    # Income
    salary_income = models.FloatField(default=0)
    business_income = models.FloatField(default=0)
    other_income = models.FloatField(default=0)

    # Deductions
    deduction_80c = models.FloatField(default=0)
    deduction_80d = models.FloatField(default=0)

    # Documents
    pan_card = models.FileField(upload_to='itr_documents/pan/', null=True, blank=True)
    aadhaar_card = models.FileField(upload_to='itr_documents/aadhaar/', null=True, blank=True)
    form_16 = models.FileField(upload_to='itr_documents/form16/', null=True, blank=True)
    bank_statement = models.FileField(upload_to='itr_documents/bank/', null=True, blank=True)

    
    # 🔹 Calculated Summary (SAVE IN DB)

# 🔹 Calculated Summary (SAVE IN DB)
    gross_income = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_deduction = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    taxable_income = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    tax_payable = models.DecimalField(max_digits=15, decimal_places=2, default=0)


    def total_income(self):
        return self.salary_income + self.business_income + self.other_income
