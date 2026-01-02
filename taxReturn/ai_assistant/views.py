from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json

# Import the ENHANCED SimpleTaxAssistant from models.py
from .models import SimpleTaxAssistant

# Initialize the ENHANCED assistant (from models.py)
assistant = SimpleTaxAssistant()

# Chat API for quick tests
@csrf_exempt
def chat_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)
    try:
        data = json.loads(request.body)
        message = data.get('message', '').strip()
        if not message:
            return JsonResponse({'error': 'Empty message'}, status=400)
        
        # Use the enhanced assistant from models.py
        result = assistant.query(message)
        
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({'success': False, 'answer': str(e)}, status=500)

# Health check
def health_check(request):
    return JsonResponse({
        'status': 'OK', 
        'message': 'Tax AI Assistant is running',
        'version': 'Enhanced v2.0'
    })

# Test page with enhanced interface
# def test_page(request):
#     return HttpResponse("""
#     <!DOCTYPE html>
#     <html>
#     <head>
#         <title>🤖 Advanced Tax AI Assistant Test</title>
#         <style>
#             body { font-family: Arial, sans-serif; padding: 20px; background: #f5f5f5; }
#             .container { max-width: 900px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
#             .test-section { margin: 25px 0; padding: 25px; border: 2px solid #4CAF50; border-radius: 8px; background: #f9f9f9; }
#             h1 { color: #2c3e50; text-align: center; }
#             h3 { color: #3498db; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
#             .btn { 
#                 padding: 12px 24px; 
#                 margin: 8px; 
#                 background: linear-gradient(135deg, #4CAF50, #2E7D32); 
#                 color: white; 
#                 border: none; 
#                 border-radius: 6px; 
#                 cursor: pointer; 
#                 font-size: 16px;
#                 font-weight: bold;
#                 transition: all 0.3s;
#             }
#             .btn:hover { 
#                 background: linear-gradient(135deg, #45a049, #1B5E20);
#                 transform: translateY(-2px);
#                 box-shadow: 0 4px 8px rgba(0,0,0,0.2);
#             }
#             .input-group { margin: 15px 0; display: flex; }
#             input[type="text"] { 
#                 padding: 12px; 
#                 flex: 1;
#                 border: 2px solid #ddd;
#                 border-radius: 6px;
#                 font-size: 16px;
#             }
#             #testResults { 
#                 margin-top: 25px; 
#                 padding: 20px; 
#                 background: white; 
#                 border-radius: 8px; 
#                 border: 2px solid #3498db;
#                 min-height: 200px;
#                 text-align: left;
#             }
#             .answer-box {
#                 background: linear-gradient(135deg, #e8f5e9, #c8e6c9);
#                 padding: 20px;
#                 border-radius: 8px;
#                 margin: 15px 0;
#                 border-left: 5px solid #4CAF50;
#             }
#             .confidence-bar {
#                 height: 10px;
#                 background: #e0e0e0;
#                 border-radius: 5px;
#                 margin: 10px 0;
#                 overflow: hidden;
#             }
#             .confidence-fill {
#                 height: 100%;
#                 background: linear-gradient(90deg, #4CAF50, #8BC34A);
#                 border-radius: 5px;
#             }
#         </style>
#     </head>
#     <body>
#         <div class="container">
#             <h1>🤖 Advanced Tax AI Assistant Test</h1>
#             <p style="text-align: center; color: #666;">Professional-level tax guidance with detailed responses</p>
            
#             <div class="test-section">
#                 <h3>📚 Quick Expert Tests:</h3>
#                 <button class="btn" onclick="testQuery('Tell me everything about 80C investments')">80C Detailed Guide</button>
#                 <button class="btn" onclick="testQuery('Complete ITR filing documents checklist')">ITR Documents</button>
#                 <button class="btn" onclick="testQuery('GST filing procedure and deadlines')">GST Compliance</button>
#                 <button class="btn" onclick="testQuery('Tax calculation for 15 lakh income new regime')">Tax Calculation</button>
#             </div>
            
#             <div class="test-section">
#                 <h3>🔍 Custom Expert Query:</h3>
#                 <div class="input-group">
#                     <input type="text" id="customQuestion" placeholder="Ask detailed tax questions (e.g., HRA calculation for Mumbai, Capital gains tax...)">
                   
#                         <button class="btn" onclick="handleCustomQuery()" style="margin-left: 10px;">Ask Expert</button>
#                 </div>
#                 <p style="color: #666; font-size: 14px; margin-top: 10px;">Try: "80C vs ELSS returns", "GST late fees calculation", "NRI property tax"</p>
#             </div>
            
#             <div class="test-section">
#                 <h3>📊 Test Results:</h3>
#                 <div id="testResults">
#                     <div style="text-align: center; color: #666; padding: 40px;">
#                         <h3>Ready for Expert Tax Consultation</h3>
#                         <p>Click any button above or ask a custom tax question</p>
#                         <p>I provide detailed, professional tax guidance with examples</p>
#                     </div>
#                 </div>
#             </div>
#         </div>
        
#         <script>
#         async function testQuery(question) {
#             const resultsDiv = document.getElementById('testResults');
#             resultsDiv.innerHTML = `
#                 <div style="text-align: center; padding: 20px;">
#                     <h3>Processing Expert Query...</h3>
#                     <p><strong>"${question}"</strong></p>
#                     <div style="width: 100px; height: 100px; margin: 20px auto; border: 5px solid #f3f3f3; border-top: 5px solid #4CAF50; border-radius: 50%; animation: spin 1s linear infinite;"></div>
#                 </div>
#             `;
            
#             try {
#                 const response = await fetch('/api/chat/', {
#                     method: 'POST',
#                     headers: {
#                         'Content-Type': 'application/json',
#                         'X-CSRFToken': getCookie('csrftoken')
#                     },
#                     body: JSON.stringify({ message: question })
#                 });
                
#                 const data = await response.json();
                
#                 if (data.success) {
#                     const confidencePercent = Math.round(data.confidence * 100);
#                     resultsDiv.innerHTML = `
#                         <h4 style="color: #2c3e50;">📝 Question: ${question}</h4>
#                         <div class="answer-box">
#                             <p style="color: #2c3e50; font-weight: bold; margin-bottom: 15px;">✅ Expert Answer:</p>
#                             <div style="font-size: 15px; line-height: 1.6;">${formatAnswer(data.answer)}</div>
                            
#                             <div style="margin-top: 20px; padding-top: 15px; border-top: 1px solid #ddd;">
#                                 <p><strong>Expertise Level:</strong> ${data.category || 'Tax Guidance'}</p>
                                
#                                 <div style="display: flex; align-items: center; margin: 10px 0;">
#                                     <span style="width: 120px;"><strong>Confidence:</strong></span>
#                                     <div class="confidence-bar" style="flex: 1;">
#                                         <div class="confidence-fill" style="width: ${confidencePercent}%"></div>
#                                     </div>
#                                     <span style="margin-left: 10px; font-weight: bold;">${confidencePercent}%</span>
#                                 </div>
                                
#                                 ${data.score ? `<p><strong>Match Score:</strong> ${data.score}/100</p>` : ''}
#                             </div>
#                         </div>
                        
#                         <div style="margin-top: 20px; padding: 15px; background: #e3f2fd; border-radius: 6px;">
#                             <p style="color: #1565c0; font-weight: bold;">💡 Follow-up Questions:</p>
#                             <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px;">
#                                 <button class="btn" onclick="testQuery('80C vs ELSS which is better?')" style="padding: 8px 16px; background: #2196F3; font-size: 14px;">80C vs ELSS</button>
#                                 <button class="btn" onclick="testQuery('GST penalty calculation')" style="padding: 8px 16px; background: #2196F3; font-size: 14px;">GST Penalties</button>
#                                 <button class="btn" onclick="testQuery('HRA exemption calculation')" style="padding: 8px 16px; background: #2196F3; font-size: 14px;">HRA Calculation</button>
#                                 <button class="btn" onclick="testQuery('Capital gains tax property')" style="padding: 8px 16px; background: #2196F3; font-size: 14px;">Capital Gains</button>
#                             </div>
#                         </div>
#                     `;
#                 } else {
#                     resultsDiv.innerHTML = `
#                         <h4>Question: ${question}</h4>
#                         <div style="background: #ffebee; padding: 20px; border-radius: 8px; border-left: 5px solid #f44336;">
#                             <p style="color: #c62828; font-weight: bold;">❌ Error:</p>
#                             <p>${data.error || data.answer || 'Unknown error'}</p>
#                             <button class="btn" onclick="testQuery(question)" style="background: #f44336; margin-top: 10px;">Try Again</button>
#                         </div>
#                     `;
#                 }
#             } catch (error) {
#                 resultsDiv.innerHTML = `
#                     <div style="background: #fff3e0; padding: 20px; border-radius: 8px; border-left: 5px solid #ff9800;">
#                         <p style="color: #ef6c00; font-weight: bold;">⚠️ Network Error:</p>
#                         <p>${error.message}</p>
#                         <p>Please check your connection and try again.</p>
#                     </div>
#                 `;
#             }
#         }
        
#         function formatAnswer(answer) {
#             // Convert markdown-like formatting to HTML
#             return answer
#                 .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
#                 .replace(/\n\n/g, '</p><p>')
#                 .replace(/\n/g, '<br>')
#                 .replace(/•/g, '•')
#                 .replace(/\d+\.\s/g, '<br>$&')
#                 .replace(/^\s*<p>/g, '<p>');
#         }
        
#         function testCustomQuery() {
#             const question = document.getElementById('customQuestion').value;
#             if (!question.trim()) {
#                 alert('Please enter a detailed tax question');
#                 return;
#             }
#             testQuery(question);
#         }
        
#         function getCookie(name) {
#             let cookieValue = null;
#             if (document.cookie && document.cookie !== '') {
#                 const cookies = document.cookie.split(';');
#                 for (let i = 0; i < cookies.length; i++) {
#                     const cookie = cookies[i].trim();
#                     if (cookie.substring(0, name.length + 1) === (name + '=')) {
#                         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
#                         break;
#                     }
#                 }
#             }
#             return cookieValue;
#         }
        
#         // Add CSS for spinner
#         const style = document.createElement('style');
#         style.textContent = `
#             @keyframes spin {
#                 0% { transform: rotate(0deg); }
#                 100% { transform: rotate(360deg); }
#             }
#         `;
#         document.head.appendChild(style);
        
#         // Auto-test on load
#         window.onload = function() {
#             setTimeout(() => {
#                 testQuery('Explain 80C tax saving options in detail');
#             }, 1000);
#         }
#         </script>
#     </body>
#     </html>
#     """)
# def test_page(request):
#     """Test page for AI Assistant - SIMPLIFIED ERROR-FREE VERSION"""
#     return HttpResponse("""
#     <!DOCTYPE html>
#     <html>
#     <head>
#         <title>🤖 Advanced Tax AI Assistant Test</title>
#         <meta http-equiv="Content-Security-Policy" content="default-src 'self' 'unsafe-inline' 'unsafe-eval';">
#         <style>
#             body { font-family: Arial, sans-serif; padding: 20px; background: #f5f5f5; margin: 0; }
#             .container { max-width: 900px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
#             .test-section { margin: 25px 0; padding: 25px; border: 2px solid #4CAF50; border-radius: 8px; background: #f9f9f9; }
#             h1 { color: #2c3e50; text-align: center; margin-top: 0; }
#             h3 { color: #3498db; border-bottom: 2px solid #3498db; padding-bottom: 10px; margin-top: 0; }
#             .btn { 
#                 padding: 12px 24px; 
#                 margin: 8px; 
#                 background: #4CAF50; 
#                 color: white; 
#                 border: none; 
#                 border-radius: 6px; 
#                 cursor: pointer; 
#                 font-size: 16px;
#                 font-weight: bold;
#             }
#             .btn:hover { background: #45a049; }
#             .input-group { margin: 15px 0; display: flex; }
#             input[type="text"] { 
#                 padding: 12px; 
#                 flex: 1;
#                 border: 2px solid #ddd;
#                 border-radius: 6px;
#                 font-size: 16px;
#             }
#             #testResults { 
#                 margin-top: 25px; 
#                 padding: 20px; 
#                 background: white; 
#                 border-radius: 8px; 
#                 border: 2px solid #3498db;
#                 min-height: 200px;
#             }
#             .answer-box {
#                 background: #e8f5e9;
#                 padding: 20px;
#                 border-radius: 8px;
#                 margin: 15px 0;
#                 border-left: 5px solid #4CAF50;
#             }
#             .spinner {
#                 width: 50px;
#                 height: 50px;
#                 margin: 20px auto;
#                 border: 5px solid #f3f3f3;
#                 border-top: 5px solid #4CAF50;
#                 border-radius: 50%;
#                 animation: spin 1s linear infinite;
#             }
#             @keyframes spin {
#                 0% { transform: rotate(0deg); }
#                 100% { transform: rotate(360deg); }
#             }
#         </style>
#     </head>
#     <body>
#         <div class="container">
#             <h1>🤖 Advanced Tax AI Assistant Test</h1>
#             <p style="text-align: center; color: #666;">Professional-level tax guidance</p>
            
#             <div class="test-section">
#                 <h3>📚 Quick Tests:</h3>
#                 <button class="btn" onclick="askQuestion('Tell me about 80C investments')">80C Guide</button>
#                 <button class="btn" onclick="askQuestion('ITR filing documents')">ITR Documents</button>
#                 <button class="btn" onclick="askQuestion('GST filing procedure')">GST Compliance</button>
#                 <button class="btn" onclick="askQuestion('Tax calculation')">Tax Calculation</button>
#             </div>
            
#             <div class="test-section">
#                 <h3>🔍 Custom Query:</h3>
#                 <div class="input-group">
#                     <input type="text" id="customQuestion" placeholder="Ask tax questions..." value="hi">
#                     <button class="btn" onclick="askCustomQuestion()" style="margin-left: 10px;">Ask Expert</button>
#                 </div>
#                 <p style="color: #666; font-size: 14px; margin-top: 10px;">Try: "80C", "GST", "ITR", "HRA"</p>
#             </div>
            
#             <div class="test-section">
#                 <h3>📊 Test Results:</h3>
#                 <div id="testResults">
#                     <div style="text-align: center; color: #666; padding: 40px;">
#                         <h3>Ready for Tax Consultation</h3>
#                         <p>Click any button or ask a question</p>
#                     </div>
#                 </div>
#             </div>
#         </div>
        
#         <script>
#         // SIMPLE ERROR-FREE VERSION - NO REGEX ERRORS
        
#         // Ask a question (called from buttons)
#         function askQuestion(question) {
#             if (!question) {
#                 question = document.getElementById('customQuestion').value.trim();
#             }
            
#             if (!question) {
#                 alert('Please enter a question');
#                 return;
#             }
            
#             showLoading(question);
#             sendToAPI(question);
#         }
        
#         // Handle custom question button
#         function askCustomQuestion() {
#             var question = document.getElementById('customQuestion').value.trim();
#             askQuestion(question);
#         }
        
#         // Show loading spinner
#         function showLoading(question) {
#             var resultsDiv = document.getElementById('testResults');
#             resultsDiv.innerHTML = `
#                 <div style="text-align: center; padding: 20px;">
#                     <h3>Processing Query...</h3>
#                     <p><strong>"${question}"</strong></p>
#                     <div class="spinner"></div>
#                 </div>
#             `;
#         }
        
#         // Send request to API
#         async function sendToAPI(question) {
#             try {
#                 // Get CSRF token
#                 var csrfToken = getCookie('csrftoken');
                
#                 // Send request
#                 var response = await fetch('/api/chat/', {
#                     method: 'POST',
#                     headers: {
#                         'Content-Type': 'application/json',
#                         'X-CSRFToken': csrfToken
#                     },
#                     body: JSON.stringify({ message: question })
#                 });
                
#                 // Parse response
#                 var data = await response.json();
                
#                 // Display results
#                 showResults(question, data);
                
#             } catch (error) {
#                 showError(question, error.message);
#             }
#         }
        
#         // Display successful results
#         function showResults(question, data) {
#             var resultsDiv = document.getElementById('testResults');
            
#             if (data.success) {
#                 var confidence = Math.round(data.confidence * 100);
                
#                 // Simple text formatting - NO REGEX
#                 var answer = data.answer || "No answer provided";
#                 answer = answer.replace(/\\n/g, '<br>'); // Simple line break replacement
                
#                 resultsDiv.innerHTML = `
#                     <h4 style="color: #2c3e50;">📝 Question: ${question}</h4>
#                     <div class="answer-box">
#                         <p style="color: #2c3e50; font-weight: bold;">✅ Expert Answer:</p>
#                         <div style="font-size: 15px; line-height: 1.6;">${answer}</div>
                        
#                         <div style="margin-top: 20px; padding-top: 15px; border-top: 1px solid #ddd;">
#                             <p><strong>Confidence:</strong> ${confidence}%</p>
#                             <p><strong>Category:</strong> ${data.category || 'Tax Advice'}</p>
#                         </div>
#                     </div>
                    
#                     <div style="margin-top: 20px; padding: 15px; background: #e3f2fd; border-radius: 6px;">
#                         <p style="color: #1565c0; font-weight: bold;">💡 Try These:</p>
#                         <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px;">
#                             <button class="btn" onclick="askQuestion('80C vs ELSS')" style="padding: 8px 16px; background: #2196F3; font-size: 14px;">80C vs ELSS</button>
#                             <button class="btn" onclick="askQuestion('GST penalties')" style="padding: 8px 16px; background: #2196F3; font-size: 14px;">GST Penalties</button>
#                             <button class="btn" onclick="askQuestion('HRA calculation')" style="padding: 8px 16px; background: #2196F3; font-size: 14px;">HRA Calculation</button>
#                         </div>
#                     </div>
#                 `;
#             } else {
#                 showError(question, data.error || data.answer || "Unknown error");
#             }
#         }
        
#         // Display error
#         function showError(question, errorMsg) {
#             var resultsDiv = document.getElementById('testResults');
#             resultsDiv.innerHTML = `
#                 <h4>Question: ${question}</h4>
#                 <div style="background: #ffebee; padding: 20px; border-radius: 8px;">
#                     <p style="color: #c62828; font-weight: bold;">❌ Error:</p>
#                     <p>${errorMsg}</p>
#                     <button class="btn" onclick="askQuestion('${question.replace(/'/g, "&#39;")}')" style="background: #f44336; margin-top: 10px;">Try Again</button>
#                 </div>
#             `;
#         }
        
#         // Get cookie value
#         function getCookie(name) {
#             var cookieValue = null;
#             if (document.cookie && document.cookie !== '') {
#                 var cookies = document.cookie.split(';');
#                 for (var i = 0; i < cookies.length; i++) {
#                     var cookie = cookies[i].trim();
#                     if (cookie.substring(0, name.length + 1) === (name + '=')) {
#                         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
#                         break;
#                     }
#                 }
#             }
#             return cookieValue;
#         }
        
#         // Initialize on page load
#         window.onload = function() {
#             // Add Enter key support
#             document.getElementById('customQuestion').addEventListener('keypress', function(event) {
#                 if (event.key === 'Enter') {
#                     askCustomQuestion();
#                 }
#             });
            
#             // Auto-test after 1 second
#             setTimeout(function() {
#                 askQuestion('Explain 80C tax saving');
#             }, 1000);
#         };
#         </script>
#     </body>
#     </html>
#     """)
# # Custom test API
def test_page(request):
    """Render the AI Assistant test page"""
    return render(request, 'test_page.html')

@csrf_exempt
def test_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            question = data.get("question", "")
            # Use the enhanced assistant
            result = assistant.query(question)
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid method"}, status=400)

# Tax calculator demo
@csrf_exempt
def tax_calculator(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            income = float(data.get('income', 0))
            deductions = float(data.get('deductions', 0))
            taxable_income = max(0, income - deductions - 50000)
            tax = taxable_income * 0.1  # Simple 10% flat
            return JsonResponse({
                'success': True,
                'taxable_income': taxable_income,
                'tax_amount': tax
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'POST required'})