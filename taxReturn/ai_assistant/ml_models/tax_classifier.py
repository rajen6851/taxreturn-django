import torch
import torch.nn as nn
from transformers import AutoModel, AutoTokenizer
import pickle
import os
from django.conf import settings

class TaxIntentClassifier(nn.Module):
    def __init__(self, model_name="bert-base-uncased", num_classes=10):
        super().__init__()
        
        # Load pre-trained BERT
        self.bert = AutoModel.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        # Classification layers
        self.dropout = nn.Dropout(0.3)
        self.classifier = nn.Linear(self.bert.config.hidden_size, num_classes)
        
        # Tax intent labels
        self.intent_labels = [
            "deduction_query",
            "filing_deadline",
            "tax_calculation", 
            "document_requirement",
            "gst_query",
            "notice_compliance",
            "investment_advice",
            "section_explanation",
            "form_filing",
            "other"
        ]
        
    def forward(self, input_ids, attention_mask):
        outputs = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask
        )
        
        pooled_output = outputs.pooler_output
        pooled_output = self.dropout(pooled_output)
        logits = self.classifier(pooled_output)
        
        return logits
    
    def predict_intent(self, text):
        """Predict tax intent from text"""
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=128
        )
        
        with torch.no_grad():
            outputs = self(**inputs)
            probabilities = torch.softmax(outputs, dim=1)
            predicted_class = torch.argmax(probabilities, dim=1).item()
            
        return {
            "intent": self.intent_labels[predicted_class],
            "confidence": float(probabilities[0][predicted_class]),
            "all_probabilities": {
                label: float(prob) 
                for label, prob in zip(self.intent_labels, probabilities[0])
            }
        }
    
    def save_model(self, path):
        """Save model to disk"""
        torch.save({
            'model_state_dict': self.state_dict(),
            'intent_labels': self.intent_labels
        }, path)
    
    @classmethod
    def load_model(cls, model_path=None):
        """Load trained model"""
        if model_path is None:
            model_path = os.path.join(
                settings.BASE_DIR, 
                'data/models/tax_intent_model.pth'
            )
        
        model = cls()
        
        if os.path.exists(model_path):
            checkpoint = torch.load(model_path, map_location=torch.device('cpu'))
            model.load_state_dict(checkpoint['model_state_dict'])
            model.intent_labels = checkpoint['intent_labels']
        else:
            print("Model not found. Using untrained model.")
        
        model.eval()
        return model