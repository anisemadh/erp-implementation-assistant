from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, List
import operator
from vector_store import load_vector_store
from dotenv import load_dotenv
from prompts import build_full_prompt
from query_enhancer import enhance_query
import os

# Load environment variables (for local) and check for API key
from dotenv import load_dotenv
load_dotenv()

# Verify API key exists before initialization
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Define the agent state
class AgentState(TypedDict):
    messages: Annotated[List, operator.add]
    context: str

class ERPAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        self.vectorstore = load_vector_store()
        self.graph = self._build_graph()
        self.last_sources = []  # Track sources from last query
    
    def classify_query_type(self, query: str) -> str:
        """Classify query to select appropriate prompt"""
        query_lower = query.lower()
    
        # Configuration keywords
        config_keywords = [
            'configure', 'setup', 'set up', 'create', 'enable', 
            'how do i', 'how to', 'setting', 'parameter'
        ]
    
        # Troubleshooting keywords
        trouble_keywords = [
            'error', 'issue', 'problem', 'not working', 'failed',
            'stuck', 'why', 'wrong', 'doesn\'t', 'can\'t', 'unable'
        ]
    
        # Best practice keywords
        practice_keywords = [
            'best practice', 'should', 'recommend', 'advice',
            'approach', 'strategy', 'optimal', 'better way'
        ]
    
        # Check for each type
        if any(word in query_lower for word in config_keywords):
            return 'configuration'
        elif any(word in query_lower for word in trouble_keywords):
            return 'troubleshooting'
        elif any(word in query_lower for word in practice_keywords):
            return 'best_practices'
        else:
            return 'general'
    
    def detect_relevant_modules(self, query: str) -> list:
        """Detect which M3 modules are relevant to the query"""
        query_lower = query.lower()
        relevant_modules = []
        
        # Module keywords
        module_keywords = {
            'OIS': ['customer order', 'sales order', 'order type', 'ois', 'order entry', 'invoice customer'],
            'PPS': ['purchase order', 'po ', 'purchasing', 'supplier', 'vendor', 'pps', 'procurement', 'receive', 'receipt'],
            'MMS': ['inventory', 'item', 'warehouse', 'stock', 'mms', 'allocation', 'on hand', 'product'],
            'CRS': ['customer master', 'customer setup', 'crs', 'credit', 'customer relations'],
            'MWS': ['delivery', 'picking', 'shipment', 'mws', 'dispatch', 'ship'],
            'ARS': ['invoice', 'accounts receivable', 'ars', 'billing'],
            'APS': ['accounts payable', 'aps', 'vendor invoice'],
        }
        
        # Check query for module indicators
        for module, keywords in module_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                relevant_modules.append(module)
        
        # If no specific module detected, return empty (search all)
        return relevant_modules
    
    def _build_graph(self):
        """Build the LangGraph workflow"""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("retrieve", self.retrieve_context)
        workflow.add_node("generate", self.generate_response)
        
        # Add edges
        workflow.add_edge("retrieve", "generate")
        workflow.add_edge("generate", END)
        
        # Set entry point
        workflow.set_entry_point("retrieve")
        
        return workflow.compile()
    
    def retrieve_context(self, state: AgentState):
        """Enhanced retrieval with query expansion and metadata filtering"""
        query = state["messages"][-1].content
        
        # 1. Enhance query with M3 terminology
        enhanced_query = enhance_query(query)
        
        # 2. Detect relevant modules
        relevant_modules = self.detect_relevant_modules(query)
        
        # 3. Search with metadata filtering
        if relevant_modules:
            docs = self.vectorstore.similarity_search(enhanced_query, k=8)
            
            # Post-filter by modules
            filtered_docs = []
            for doc in docs:
                module_str = doc.metadata.get('module_str', '')
                doc_modules = module_str.split(',') if module_str else []
                if any(module in doc_modules for module in relevant_modules):
                    filtered_docs.append(doc)
            
            docs = filtered_docs[:5]
            print(f"✓ Filtered to {len(docs)} chunks from modules: {', '.join(relevant_modules)}")
        else:
            docs = self.vectorstore.similarity_search(enhanced_query, k=5)
            print(f"✓ Retrieved {len(docs)} chunks (all modules)")
        
        # 4. Build context
        context = "\n\n".join([
            f"[Source: {doc.metadata.get('source', 'Unknown')}]\n{doc.page_content}"
            for doc in docs
        ])
        
        # Store sources for later retrieval
        self.last_sources = [
            {
                'source': doc.metadata.get('source', 'Unknown'),
                'module': doc.metadata.get('module_str', 'Unknown'),
                'doc_type': doc.metadata.get('doc_type', 'Unknown')
            } 
            for doc in docs
        ]
        
        return {"context": context}
    
    def generate_response(self, state: AgentState):
        """Generate response using LLM with retrieved context"""
        context = state["context"]
        query = state["messages"][-1].content

        # Classify query type
        query_type = self.classify_query_type(query)
        print(f"📋 Query type: {query_type}")

        # Build context-aware system prompt
        system_prompt = build_full_prompt(query_type, context)

        # Generate response (same as before)
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=query)
        ]

        response = self.llm.invoke(messages)

        return {"messages": [response]}

    def generate_response_stream(self, query: str, context: str, query_type: str):
        """Generate streaming response - for Streamlit"""
        system_prompt = build_full_prompt(query_type, context)
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=query)
        ]
        
        # Stream response
        for chunk in self.llm.stream(messages):
            if chunk.content:
                yield chunk.content
    
    def run(self, query: str, conversation_history=None):
        """Run the agent with a query and optional conversation history"""
        if conversation_history is None:
            conversation_history = []
        
        initial_state = {
            "messages": conversation_history + [HumanMessage(content=query)],
            "context": ""
        }
        
        result = self.graph.invoke(initial_state)
        return result["messages"][-1].content, result["messages"]
    
    def get_last_sources(self):
        """Get sources from the last query"""
        return self.last_sources

if __name__ == "__main__":
    agent = ERPAgent()
    
    # Test with a sample query
    response = agent.run("How do I set up supplier rebate?")
    print("\n" + "="*50)
    print("Response:")
    print(response)