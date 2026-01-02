def calculate_itr_summary(itr):
    salary = itr.salary_income or 0
    business = itr.business_income or 0
    other = itr.other_income or 0

    d80c = itr.deduction_80c or 0
    d80d = itr.deduction_80d or 0

    gross = salary + business + other
    deduction = d80c + d80d
    taxable = max(gross - deduction, 0)

    tax = 0
    if taxable <= 300000:
        tax = 0
    elif taxable <= 600000:
        tax = (taxable - 300000) * 0.05
    elif taxable <= 900000:
        tax = 15000 + (taxable - 600000) * 0.10
    elif taxable <= 1200000:
        tax = 45000 + (taxable - 900000) * 0.15
    elif taxable <= 1500000:
        tax = 90000 + (taxable - 1200000) * 0.20
    else:
        tax = 150000 + (taxable - 1500000) * 0.30

    itr.gross_income = gross
    itr.total_deduction = deduction
    itr.taxable_income = taxable
    itr.tax_payable = round(tax)

    return itr
