
# ERP Implementation Assistant

An AI-powered assistant for Infor ERP implementation using RAG (Retrieval-Augmented Generation) and LangGraph.

## Features
- Answers questions about Infor ERP configuration
- Retrieves relevant information from documented knowledge base
- Maintains conversation context for follow-up questions
- Provides implementation guidance based on real consulting experience
- View source documents for transparency
- Interactive web interface

## Current Coverage
- Customer Order Management
- Purchasing and Inventory Management
- Supplier Approval Workflows
- Vendor Rebate Configuration
- Sales Order Management
- Supply Chain Execution

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/anisemadh/erp-implementation-assistant.git
   cd erp-implementation-assistant
   ```

2. **Create virtual environment and install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root with:
   ```
   OPENAI_API_KEY=your-openai-key-here
   LANGCHAIN_TRACING_V2=true
   LANGCHAIN_API_KEY=your-langsmith-key-here
   LANGCHAIN_PROJECT=erp-assistant
   ```

4. **Add your Infor documentation**
   - Place PDF files in `docs/` folder
   - Add markdown content to `docs/infor_knowledge.md`

5. **Build the knowledge base**
   ```bash
   python src/vector_store.py
   ```

## How to Run

### Web Interface (Recommended)
```bash
streamlit run src/app.py
```
Then open http://localhost:8501 in your browser.

**Features:**
- Interactive chat with conversation memory
- View source documents for each response
- Example questions to get started
- Session statistics
- Clear conversation history

### Command Line
```bash
python src/chat.py
```

## Technical Stack
- **LangChain** - RAG pipeline and document processing
- **LangGraph** - Agent orchestration and workflow
- **ChromaDB** - Vector storage for embeddings
- **OpenAI GPT-4** - Language model
- **Streamlit** - Web interface
- **LangSmith** - Tracing and monitoring

## Project Structure
```
├── src/
│   ├── agent.py
│   ├── vector_store.py
│   ├── ingest_docs.py
│   ├── chat.py
│   ├── app.py
│   └── visualize_graph.py
├── docs/
│   ├── infor_knowledge.md
│   └── *.pdf
├── data/
│   └── chroma_db/
└── tests/
    └── test_retrieval.py
```

## Development

To visualize the agent workflow:
```bash
python src/visualize_graph.py
```

To test retrieval:
```bash
python src/test_retrieval.py
```

## Project Status
- [x] RAG system with vector database
- [x] LangGraph agent workflow
- [x] Interactive chat interface (CLI and Web)
- [x] Conversation memory
- [x] PDF document processing
- [x] Source document display
- [x] LangSmith integration
- [ ] Enhanced prompt engineering
- [ ] Cloud deployment
- [ ] Additional Infor modules
```

