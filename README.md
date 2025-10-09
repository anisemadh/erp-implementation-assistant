# ERP Implementation Assistant

An AI-powered assistant for Infor ERP implementation using RAG (Retrieval-Augmented Generation) and LangGraph.

## Features
- Answers questions about Infor ERP configuration
- Retrieves relevant information from documented knowledge base
- Maintains conversation context for follow-up questions
- Provides implementation guidance based on real consulting experience

## Current Coverage
- Customer Order Management
- Purchasing and Inventory Management
- Supplier Approval Workflows
- Vendor Rebate Configuration
## Knowledge Base
- Infor Knowledge (markdown) 
    - Customer Order Management (markdown)
    - Purchasing and Inventory Management (markdown)
- Purchasing Module (PDF)
- Sales Order Management Module (PDF)
- Supply Chain Execution Module (PDF)

## Supported Document Types
- Markdown (.md)
- PDF (.pdf)

## How to Run

### Web Interface (Recommended)
```bash
streamlit run src/app.py