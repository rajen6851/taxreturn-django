from django.db import models

class SimpleTaxAssistant:
    """
    Enhanced Indian Tax Assistant with detailed knowledge
    """
    def __init__(self):
        self.knowledge_base = self._create_enhanced_knowledge_base()
        print("🤖 Enhanced Tax Assistant Initialized")
        print(f"📚 Knowledge Base: {len(self.knowledge_base)} expert tax categories loaded")
    
    def _create_enhanced_knowledge_base(self):
        """Create comprehensive Indian tax knowledge base"""
        return {
            "80c": {
                "answer": """
                **📊 Section 80C - Comprehensive Tax Saving Guide**
                
                **💰 Maximum Deduction:** ₹1,50,000 per financial year
                
                **📋 Eligible Investment Options:**
                
                1. **Public Provident Fund (PPF)**
                   - Lock-in: 15 years (partial withdrawal after 7 years)
                   - Interest Rate: ~7.1% p.a. (quarterly compounding)
                   - Risk: Government-backed, zero risk
                   - Tax: EEE (Exempt-Exempt-Exempt) status
                
                2. **Equity Linked Savings Scheme (ELSS)**
                   - Lock-in: 3 years (shortest among 80C options)
                   - Returns: Market-linked (12-15% historical average)
                   - Risk: Moderate to High (equity exposure)
                   - Tax: LTCG tax @10% above ₹1 lakh
                
                3. **National Savings Certificate (NSC)**
                   - Lock-in: 5 years
                   - Interest: 7.7% p.a. (compounded annually but payable at maturity)
                   - Risk: Government-backed
                   - TDS: No TDS, interest taxable annually
                
                4. **Tax Saving Fixed Deposit**
                   - Lock-in: 5 years
                   - Interest: 6.5-7.5% p.a. (bank dependent)
                   - Risk: Low (up to ₹5 lakh DICGC insurance)
                   - TDS: Applicable if interest > ₹40,000
                
                5. **Life Insurance Premiums**
                   - Policy must be on self, spouse, or children
                   - Minimum coverage: 10 times annual premium for traditional policies
                   - ULIPs also eligible but check lock-in
                
                6. **Home Loan Principal Repayment**
                   - Only for self-occupied property
                   - Maximum: Actual principal repaid during the year
                   - Additional benefit: Section 24(b) for interest deduction
                
                7. **Sukanya Samriddhi Yojana (SSY)**
                   - For girl child below 10 years
                   - Interest: 8.2% p.a. (2024-25)
                   - Maximum deposit: ₹1.5 lakh per year
                   - Complete withdrawal at age 21 or marriage (after 18)
                
                8. **Tuition Fees**
                   - Maximum 2 children
                   - Only tuition fees (not development fees, transport, etc.)
                   - School/college/institution in India only
                
                **📄 Required Documents:**
                • Investment receipts with date and amount
                • Form 16/16A for TDS deducted
                • Bank statements showing transactions
                • Policy certificates for insurance
                • School fee receipts with institution details
                
                **💡 Pro Tips:**
                • Start early in financial year for compounding benefits
                • Diversify across instruments for risk management
                • Maintain proper records for 6+ years
                • Consider combining with NPS for additional ₹50,000 deduction (Section 80CCD)
                """,
                "keywords": ["80c", "section 80c", "80 c", "eighty c", "tax saving", "deduction", "investment", "ppf", "elss", "nsc", "fd", "insurance", "home loan", "ssy", "tuition"],
                "confidence": 0.97
            },
            "itr": {
                "answer": """
                **📑 ITR Filing - Complete Document Checklist & Process**
                
                **⏰ Important Deadlines:**
                • Normal Filing: **July 31** of assessment year
                • Belated Return: **December 31** (with penalty)
                • Revised Return: Before assessment completion or 1 year
                
                **📋 Mandatory Documents Checklist:**
                
                **A. Personal Documents:**
                1. **PAN Card** (Permanent Account Number)
                2. **Aadhaar Card** (Linked with PAN)
                3. **Bank Account Details** (IFSC, Account Number)
                4. **Form 26AS** (Annual Tax Statement - Download from TRACES)
                
                **B. Income Proofs:**
                1. **Form 16** (Part A & B) - For salaried employees
                2. **Salary Slips** (April to March)
                3. **Interest Certificates** from banks/post office
                4. **Rent Receipts** (if rental income > ₹50,000/month)
                5. **Capital Gains Statements** from broker (for stocks/MFs)
                6. **Business Income Details** (Profit & Loss statement, Balance Sheet)
                
                **C. Deduction Proofs (Section-wise):**
                
                **1. Section 80C (₹1.5 lakh):**
                   • PPF passbook/statement
                   • ELSS investment proof
                   • NSC certificates
                   • Insurance premium receipts (with policy number)
                   • Home loan principal certificate from bank
                   • Tuition fee receipts (children)
                
                **2. Section 80D (Health Insurance):**
                   • Premium payment receipts (self, spouse, children, parents)
                   • Policy documents
                   • Age proof for senior citizen parents
                
                **3. House Rent Allowance (HRA):**
                   • Rent receipts (monthly, signed by landlord)
                   • Rent agreement (registered if rent > ₹50,000/month)
                   • Landlord PAN (if annual rent > ₹1,00,000)
                
                **4. Home Loan Interest (Section 24):**
                   • Interest certificate from bank (showing breakup)
                   • Possession certificate (for under-construction property)
                
                **D. Other Important Documents:**
                1. **Donation Receipts** (80G) - with registration number
                2. **Medical Bills** (80DDB) - for specified diseases
                3. **Education Loan Interest** (80E) - certificate from bank
                4. **NPS Contribution** (80CCD) - statement
                
                **🔄 ITR Forms Guide:**
                
                • **ITR-1 (Sahaj):** For salaried individuals with income up to ₹50 lakh
                • **ITR-2:** For individuals with capital gains, multiple house properties
                • **ITR-3:** For individuals having income from business/profession
                • **ITR-4 (Sugam):** For presumptive taxation (44AD/44ADA)
                """,
                "keywords": ["itr", "income tax return", "filing", "form 16", "documents", "checklist", "deadline", "26as", "efiling"],
                "confidence": 0.96
            },
            "gst": {
                "answer": """
                **🏢 GST Compliance - Complete Filing Guide**
                
                **📊 GST Registration Threshold:**
                • **Normal States:** ₹40 lakh turnover (goods), ₹20 lakh (services)
                • **Special Category States:** ₹20 lakh turnover (goods), ₹10 lakh (services)
                
                **⏰ Monthly/Quarterly Due Dates:**
                
                **🔹 Monthly Filers:**
                • **GSTR-1** (Outward supplies): 11th of next month
                • **GSTR-3B** (Summary return): 20th of next month
                • **GSTR-9** (Annual return): 31st December of next FY
                
                **🔸 Quarterly Filers (QRMP Scheme):**
                • **GSTR-1:** 13th of month following quarter
                • **GSTR-3B:** 22nd/24th of month following quarter
                
                **💰 Late Fees Structure:**
                • **Nil Return:** ₹20 per day (max ₹5,000)
                • **Taxable Return:** ₹50 per day (max ₹10,000)
                • **Interest:** 18% p.a. on late tax payment
                
                **📋 GST Return Types:**
                
                1. **GSTR-1:** Details of outward supplies
                   - Invoice-wise details
                   - B2B, B2C (>₹2.5 lakh), B2C (others summary)
                   - Export/SEZ supplies
                   - Credit/Debit notes
                
                2. **GSTR-3B:** Monthly summary return
                   - Summary of outward supplies
                   - Input tax credit claimed
                   - Tax payable and payment
                   - Late fee and interest
                
                3. **GSTR-9:** Annual return
                   - Consolidated details for the year
                   - Reconciliation with financials
                   - HSN summary of outward supplies
                
                4. **GSTR-9C:** Reconciliation statement
                   - Required if turnover > ₹5 crore
                   - Certified by CA/CMA
                """,
                "keywords": ["gst", "gstr", "gst filing", "gstr-1", "gstr-3b", "gstr-9", "input tax credit", "itc"],
                "confidence": 0.95
            },
            "tax_calculation": {
                "answer": """
                **💰 Income Tax Calculation - FY 2024-25 (AY 2025-26)**
                
                **📊 New Tax Regime (Default from FY 2023-24):**
                
                | Income Slab (₹)          | Tax Rate | Quick Calculation |
                |--------------------------|----------|-------------------|
                | 0 - 3,00,000            | 0%       | Nil               |
                | 3,00,001 - 7,00,000     | 5%       | 5% of (Income - 3L) |
                | 7,00,001 - 10,00,000    | 10%      | ₹20,000 + 10% of (Inc - 7L) |
                | 10,00,001 - 12,00,000   | 15%      | ₹50,000 + 15% of (Inc - 10L) |
                | 12,00,001 - 15,00,000   | 20%      | ₹80,000 + 20% of (Inc - 12L) |
                | Above 15,00,000         | 30%      | ₹1,40,000 + 30% of (Inc - 15L) |
                
                **🎯 Standard Deduction:** ₹75,000 for salaried individuals
                
                **📈 Old Tax Regime (Optional):**
                
                | Income Slab (₹)          | Tax Rate | Surcharge (>₹50L) |
                |--------------------------|----------|-------------------|
                | 0 - 2,50,000            | 0%       | -                |
                | 2,50,001 - 5,00,000     | 5%       | -                |
                | 5,00,001 - 10,00,000    | 20%      | -                |
                | Above 10,00,000         | 30%      | 10-37%           |
                
                **✅ Available Deductions (Old Regime Only):**
                1. **Section 80C:** ₹1,50,000
                2. **Section 80D:** ₹25,000 (₹50,000 for senior parents)
                3. **HRA:** As per calculation
                4. **Home Loan Interest:** ₹2,00,000 (self-occupied)
                5. **LTA:** Actual bills (2 trips in 4 years)
                6. **Standard Deduction:** ₹50,000
                
                **🧮 Example Calculation - New Regime:**
                
                **Case:** ₹18,00,000 annual income (Salaried)
                
                **Step 1: Gross Income = ₹18,00,000**
                
                **Step 2: Less Standard Deduction = ₹75,000**
                Taxable Income = ₹18,00,000 - ₹75,000 = ₹17,25,000
                
                **Step 3: Tax Calculation:**
                • First ₹3,00,000: ₹0
                • Next ₹4,00,000 (3L-7L): 5% of ₹4,00,000 = ₹20,000
                • Next ₹3,00,000 (7L-10L): 10% of ₹3,00,000 = ₹30,000
                • Next ₹2,00,000 (10L-12L): 15% of ₹2,00,000 = ₹30,000
                • Next ₹3,00,000 (12L-15L): 20% of ₹3,00,000 = ₹60,000
                • Balance ₹2,25,000 (15L-17.25L): 30% of ₹2,25,000 = ₹67,500
                
                **Step 4: Total Tax = ₹20,000 + ₹30,000 + ₹30,000 + ₹60,000 + ₹67,500 = ₹2,07,500**
                
                **Step 5: Add Cess @4% = ₹2,07,500 × 4% = ₹8,300**
                
                **Step 6: Final Tax Liability = ₹2,07,500 + ₹8,300 = ₹2,15,800**
                """,
                "keywords": ["tax calculation", "income tax", "tax slab", "new regime", "old regime", "standard deduction", "how much tax"],
                "confidence": 0.98
            }
        }
    
    def find_answer(self, user_query):
        user_query = user_query.lower().strip()
        best_match = None
        best_score = 0

        for key, info in self.knowledge_base.items():
            score = 0
            for keyword in info.get("keywords", []):
                if keyword in user_query:
                    score += 3
            if key in user_query:
                score += 5
            
            # Enhanced matching
            if key == "80c" and any(word in user_query for word in ["section 80", "80 c", "eighty c"]):
                score += 4
            
            if key == "itr" and any(word in user_query for word in ["income tax return", "tax return"]):
                score += 4
            
            if "tax calculation" in user_query or "how much tax" in user_query:
                score += 6
            
            if score > best_score:
                best_score = score
                best_match = info

        return best_match, best_score

    def query(self, question, user_context=None):
        try:
            match, score = self.find_answer(question)

            if match and score > 2:
                answer = match['answer']
                confidence = match['confidence']
                return {
                    "success": True,
                    "answer": answer,
                    "confidence": confidence,
                    "score": score,
                    "category": "Tax Guidance",
                }
            else:
                return {
                    "success": True,
                    "answer": """
                    **🤖 Welcome to Advanced Tax AI Assistant!**
                    
                    I specialize in detailed Indian tax guidance. Please ask specific questions like:
                    
                    **📊 Tax Planning:**
                    • "80C investment options detailed comparison"
                    • "Tax saving for ₹15 lakh income"
                    • "PPF vs ELSS which is better?"
                    
                    **📑 Compliance:**
                    • "ITR filing documents checklist"
                    • "GST monthly filing procedure"
                    • "TDS rates and deadlines"
                    
                    **💰 Calculations:**
                    • "Tax calculation for ₹10 lakh income"
                    • "HRA exemption calculation for Mumbai"
                    • "Capital gains tax on property sale"
                    
                    **🏠 Property Tax:**
                    • "Home loan tax benefits"
                    • "Property sale capital gains"
                    • "Rental income taxation"
                    
                    Ask me anything specific for detailed professional guidance!
                    """,
                    "confidence": 0.5,
                    "score": score,
                    "category": "General",
                }
        except Exception as e:
            return {
                "success": False,
                "answer": f"**Technical Error:** {str(e)}",
                "confidence": 0.0,
                "category": "Error"
            }