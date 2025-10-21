from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, List
import operator
from vector_store import load_vector_store
from dotenv import load_dotenv
from prompts import build_full_prompt
from query_enhancer import enhance_query

load_dotenv()

# Define the agent state
class AgentState(TypedDict):
    messages: Annotated[List, operator.add]
    context: str

class ERPAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        self.vectorstore = load_vector_store()
        self.graph = self._build_graph()
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
        """Enhanced retrieval with query expansion"""
        query = state["messages"][-1].content
        
        # Enhance query with M3 terminology
        enhanced_query = enhance_query(query)
        print(f"\nOriginal query: {query}")
        print(f"Enhanced query: {enhanced_query}\n")
        
        # Search with enhanced query
        docs = self.vectorstore.similarity_search(enhanced_query, k=5)
        
        context = "\n\n".join([
            f"[Source: {doc.metadata.get('source', 'Unknown')}]\n{doc.page_content}"
            for doc in docs
        ])
        
        return {"context": context}
    
    def generate_response(self, state: AgentState):
        """Generate response using LLM with retrieved context"""
        context = state["context"]
        query = state["messages"][-1].content
    
        # Classify query type
        query_type = self.classify_query_type(query)
        print(f"Query classified as: {query_type}")
    
        # Build context-aware system prompt
        system_prompt = build_full_prompt(query_type, context)
    
        # Generate response
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=query)
        ]
    
        response = self.llm.invoke(messages)
    
        return {"messages": [response]}
    
    # Update the run method in ERPAgent class:
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

if __name__ == "__main__":
    agent = ERPAgent()
    
    # Test with a sample query
    response = agent.run("How do I set up supplier rebate?")
    print("\n" + "="*50)
    print("Response:")
    print(response)
