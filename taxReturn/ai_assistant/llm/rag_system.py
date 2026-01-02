import os
from typing import Dict
from django.conf import settings

# Import के लिए try-catch block use करें
try:
    # LangChain के different versions के लिए
    from langchain.chains import RetrievalQA
    from langchain.prompts import PromptTemplate
    from langchain_community.llms import HuggingFacePipeline
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_community.vectorstores import FAISS
    from langchain_community.document_loaders import PyPDFLoader, TextLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain.schema import Document
    LANGCHAIN_AVAILABLE = True
    print("✅ LangChain imports successful")
except ImportError as e:
    # Alternative imports try करें
    try:
        # Older versions के लिए
        from langchain import PromptTemplate
        from langchain.chains import RetrievalQA
        from langchain.llms import HuggingFacePipeline
        from langchain.embeddings import HuggingFaceEmbeddings
        from langchain.vectorstores import FAISS
        from langchain.document_loaders import PyPDFLoader, TextLoader
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        from langchain.docstore.document import Document
        LANGCHAIN_AVAILABLE = True
        print("✅ LangChain (older version) imports successful")
    except ImportError:
        LANGCHAIN_AVAILABLE = False
        print("❌ LangChain not available")

from transformers import pipeline
import pickle


class TaxRAGSystem:
    """Retrieval Augmented Generation System for Indian Tax Queries"""

    def __init__(self):
        if not LANGCHAIN_AVAILABLE:
            raise ImportError(
                "LangChain not installed. Please install: "
                "pip install langchain==0.0.340 langchain-community==0.0.10"
            )
        
        self.embedding_model = None
        self.vector_store = None
        self.llm = None
        self.qa_chain = None

        self.vector_store_path = os.path.join(
            settings.BASE_DIR,
            "data/processed/embeddings/tax_faiss_index"
        )

        self._initialize_components()

    # --------------------------------------------------
    # INITIALIZATION
    # --------------------------------------------------

    def _initialize_components(self):
        print("🔄 Initializing TaxRAGSystem...")
        
        # 1. Initialize embeddings
        self.embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",  # Smaller, faster model
            model_kwargs={"device": "cpu"}
        )
        
        # 2. Load or create vector store
        self.vector_store = self._load_vector_store()
        
        # 3. Initialize LLM
        self.llm = self._initialize_llm()
        
        # 4. Build QA chain
        self.qa_chain = self._build_qa_chain()
        
        print("✅ TaxRAGSystem initialized successfully")

    def _initialize_llm(self):
        """Initialize Language Model"""
        print("🔄 Initializing LLM...")
        
        try:
            # Try smaller model first (faster)
            model_id = "google/flan-t5-small"
            
            pipe = pipeline(
                "text2text-generation",
                model=model_id,
                tokenizer=model_id,
                max_length=256,  # Reduced for faster responses
                temperature=0.3,
                do_sample=True
            )
            
            print(f"✅ LLM loaded: {model_id}")
            return HuggingFacePipeline(pipeline=pipe)
            
        except Exception as e:
            print(f"⚠️ Error loading LLM: {e}")
            # Fallback to dummy LLM
            return self._create_dummy_llm()

    def _create_dummy_llm(self):
        """Create a dummy LLM for testing"""
        from langchain.llms.base import BaseLLM
        
        class DummyLLM(BaseLLM):
            def _call(self, prompt, stop=None):
                return "I'm a dummy LLM for testing. Please install proper models."
            
            def _identifying_params(self):
                return {"name": "DummyLLM"}
        
        return DummyLLM()

    # --------------------------------------------------
    # VECTOR STORE
    # --------------------------------------------------

    def _load_vector_store(self):
        if os.path.exists(self.vector_store_path):
            print("✅ Loading existing FAISS index")
            try:
                return FAISS.load_local(
                    self.vector_store_path,
                    self.embedding_model,
                    allow_dangerous_deserialization=True
                )
            except Exception as e:
                print(f"⚠️ Error loading FAISS index: {e}")
                return self._create_vector_store()
        else:
            print("🆕 Creating new FAISS index")
            return self._create_vector_store()

    def _create_vector_store(self):
        documents = self._load_tax_documents()
        
        if not documents:
            documents = self._basic_tax_knowledge()
        
        # Create directory if not exists
        os.makedirs(os.path.dirname(self.vector_store_path), exist_ok=True)
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,  # Reduced for faster processing
            chunk_overlap=100
        )

        chunks = splitter.split_documents(documents)
        print(f"📄 Total chunks created: {len(chunks)}")

        vector_store = FAISS.from_documents(chunks, self.embedding_model)
        
        try:
            vector_store.save_local(self.vector_store_path)
            print(f"💾 Vector store saved to: {self.vector_store_path}")
        except Exception as e:
            print(f"⚠️ Error saving vector store: {e}")

        return vector_store

    # --------------------------------------------------
    # DOCUMENT LOADING
    # --------------------------------------------------

    def _load_tax_documents(self):
        tax_data_path = os.path.join(settings.BASE_DIR, "data/raw/")
        documents = []
        
        # Create directory if not exists
        os.makedirs(tax_data_path, exist_ok=True)

        # Check if directory exists and has files
        if not os.path.exists(tax_data_path):
            print(f"📁 Creating directory: {tax_data_path}")
            os.makedirs(tax_data_path, exist_ok=True)
            return []
        
        # Load PDFs
        pdf_files = [f for f in os.listdir(tax_data_path) if f.endswith('.pdf')]
        for pdf_file in pdf_files[:2]:  # Limit to 2 PDFs for testing
            try:
                pdf_path = os.path.join(tax_data_path, pdf_file)
                loader = PyPDFLoader(pdf_path)
                docs = loader.load()
                documents.extend(docs)
                print(f"✔ Loaded PDF: {pdf_file} ({len(docs)} pages)")
            except Exception as e:
                print(f"❌ Error loading {pdf_file}: {e}")
        
        # Load text files
        txt_files = [f for f in os.listdir(tax_data_path) if f.endswith('.txt')]
        for txt_file in txt_files[:2]:  # Limit to 2 text files
            try:
                txt_path = os.path.join(tax_data_path, txt_file)
                loader = TextLoader(txt_path)
                docs = loader.load()
                documents.extend(docs)
                print(f"✔ Loaded text file: {txt_file}")
            except Exception as e:
                print(f"❌ Error loading {txt_file}: {e}")

        return documents

    def _basic_tax_knowledge(self):
        """Create basic tax knowledge if no documents found"""
        print("📝 Creating basic tax knowledge...")
        
        return [
            Document(
                page_content="""
                SECTION 80C - DEDUCTIONS
                Maximum deduction: ₹1,50,000 per financial year
                Eligible investments: 
                • Public Provident Fund (PPF)
                • Equity Linked Savings Scheme (ELSS)
                • National Savings Certificate (NSC)
                • Tax-saving Fixed Deposits (5-year lock-in)
                • Life Insurance Premiums
                • Principal repayment of Home Loan
                • Sukanya Samriddhi Yojana
                • Tuition fees for children
                """,
                metadata={"source": "Income Tax Act", "section": "80C", "type": "deduction"}
            ),
            Document(
                page_content="""
                STANDARD DEDUCTION - SECTION 16
                • Available for salaried individuals
                • Amount: ₹50,000 per financial year
                • Automatically deducted from salary income
                • No proof required
                """,
                metadata={"source": "Income Tax Act", "section": "16", "type": "deduction"}
            ),
            Document(
                page_content="""
                GST FILING DEADLINES
                For regular taxpayers (monthly):
                • GSTR-1: 11th of next month
                • GSTR-3B: 20th of next month
                
                For quarterly taxpayers:
                • GSTR-1: 13th of month following quarter
                • GSTR-3B: 22nd/24th of month following quarter
                
                Late fee: ₹50 per day (₹20 for nil return)
                """,
                metadata={"source": "GST Act", "section": "GSTR", "type": "compliance"}
            ),
            Document(
                page_content="""
                HRA EXEMPTION CALCULATION
                Exemption is minimum of:
                1. Actual HRA received
                2. 50% of basic salary (for metro cities)
                3. 40% of basic salary (for non-metro cities)
                4. Rent paid minus 10% of basic salary
                
                Required documents:
                • Rent receipts
                • Rent agreement
                • Landlord PAN (if rent > ₹1,00,000 per year)
                """,
                metadata={"source": "Income Tax Rules", "section": "HRA", "type": "exemption"}
            ),
            Document(
                page_content="""
                INCOME TAX SLABS 2023-24 (NEW REGIME)
                • 0 - ₹3,00,000: 0%
                • ₹3,00,001 - ₹6,00,000: 5%
                • ₹6,00,001 - ₹9,00,000: 10%
                • ₹9,00,001 - ₹12,00,000: 15%
                • ₹12,00,001 - ₹15,00,000: 20%
                • Above ₹15,00,000: 30%
                
                Standard deduction: ₹50,000
                """,
                metadata={"source": "Income Tax Act", "section": "Slabs", "type": "calculation"}
            )
        ]

    # --------------------------------------------------
    # QA CHAIN
    # --------------------------------------------------

    def _build_qa_chain(self):
        """Build the QA chain with prompt template"""
        
        prompt_template = """You are an expert Indian Tax Consultant with deep knowledge of:
        - Income Tax Act, 1961 and all amendments
        - GST Laws and Rules
        - CBDT Circulars and Notifications
        - Tax Tribunal Judgments
        - Latest Budget provisions

        Use the following context to answer the question.
        If you don't know the answer, say you don't know. Don't make up answers.

        Context:
        {context}

        Question: {question}

        Provide a detailed, accurate answer with:
        1. Relevant sections and clauses
        2. Applicable limits and exemptions
        3. Compliance requirements
        4. Document requirements if any
        5. Deadlines if applicable

        Format your answer with clear headings and bullet points.

        Answer:"""

        try:
            prompt = PromptTemplate(
                template=prompt_template,
                input_variables=["context", "question"]
            )
        except:
            # For older versions
            prompt = PromptTemplate(
                input_variables=["context", "question"],
                template=prompt_template
            )

        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(
                search_kwargs={"k": 3}  # Reduced for faster search
            ),
            chain_type_kwargs={"prompt": prompt},
            return_source_documents=True
        )

    # --------------------------------------------------
    # QUERY API
    # --------------------------------------------------

    def query(self, question: str, user_context: Dict = None) -> Dict:
        """Process a tax query and return answer"""
        try:
            print(f"\n📩 Query: {question}")
            
            # Enhance question with user context
            enhanced_question = self._enhance_question(question, user_context)
            
            # Get answer from QA chain
            result = self.qa_chain({"query": enhanced_question})
            
            # Process and format response
            answer = result["result"].strip()
            sources = self._format_sources(result.get("source_documents", []))
            confidence = self._calculate_confidence(answer, sources)
            
            print(f"✅ Answer generated (confidence: {confidence:.2f})")
            
            return {
                "answer": answer,
                "sources": sources,
                "confidence": confidence,
                "success": True
            }

        except Exception as e:
            print(f"❌ Error in query: {e}")
            return {
                "answer": f"I apologize, but I encountered an error: {str(e)}. Please try again with a different question.",
                "sources": [],
                "confidence": 0.0,
                "success": False
            }

    def _enhance_question(self, question, user_context):
        """Enhance question with user context"""
        if not user_context:
            return question
        
        enhancements = []
        
        if "income" in user_context and user_context["income"]:
            enhancements.append(f"Income: ₹{user_context['income']}")
        
        if "age" in user_context and user_context["age"]:
            enhancements.append(f"Age: {user_context['age']} years")
        
        if "residential_status" in user_context and user_context["residential_status"]:
            enhancements.append(f"Residential status: {user_context['residential_status']}")
        
        if enhancements:
            return f"{question} [Context: {', '.join(enhancements)}]"
        
        return question

    def _format_sources(self, documents):
        """Format source documents for response"""
        sources = []
        
        for doc in documents[:2]:  # Return top 2 sources
            source_info = {
                "content": doc.page_content[:150] + "...",
                "metadata": doc.metadata
            }
            sources.append(source_info)
        
        return sources

    def _calculate_confidence(self, answer, sources):
        """Calculate confidence score for answer"""
        if not answer or "don't know" in answer.lower() or "apologize" in answer.lower():
            return 0.3
        
        if sources:
            return 0.8  # Good confidence with sources
        
        if len(answer) > 50:  # Substantial answer
            return 0.7
        
        return 0.5  # Moderate confidence

    # --------------------------------------------------
    # UTILITY METHODS
    # --------------------------------------------------

    def get_status(self):
        """Get system status"""
        return {
            "status": "ready",
            "vector_store_loaded": self.vector_store is not None,
            "llm_loaded": self.llm is not None,
            "vector_store_path": self.vector_store_path,
            "document_count": len(self.vector_store.index_to_docstore_id) if self.vector_store else 0
        }

    def clear_cache(self):
        """Clear vector store cache"""
        import shutil
        if os.path.exists(self.vector_store_path):
            shutil.rmtree(os.path.dirname(self.vector_store_path))
            print("🧹 Cache cleared")
            return True
        return False


# Global instance for easy access
tax_rag_system = None

def get_tax_rag_system():
    """Get or create TaxRAGSystem instance"""
    global tax_rag_system
    if tax_rag_system is None:
        try:
            tax_rag_system = TaxRAGSystem()
        except Exception as e:
            print(f"❌ Failed to initialize TaxRAGSystem: {e}")
            tax_rag_system = None
    return tax_rag_system