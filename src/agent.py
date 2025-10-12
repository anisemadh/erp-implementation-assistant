from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, List
import operator
from vector_store import load_vector_store
from dotenv import load_dotenv

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
        """Retrieve relevant context from vector store"""
        query = state["messages"][-1].content
    
        # Search for relevant documents
        docs = self.vectorstore.similarity_search(query, k=5)
    
        # Combine retrieved documents into context
        context = "\n\n".join([doc.page_content for doc in docs])
    
        print(f"Retrieved {len(docs)} relevant documents")
        print("\nRetrieved context preview:")  # ADD THIS
        print(context[:500])  # ADD THIS - shows first 500 chars
        print("...\n")  # ADD THIS
    
        return {"context": context}
    
    def generate_response(self, state: AgentState):
        """Generate response using LLM with retrieved context"""
        context = state["context"]
        query = state["messages"][-1].content
        
        # Create system message with context
        system_msg = f"""You are an expert Infor ERP implementation consultant. 
Use the following context from the knowledge base to answer the user's question.
If the context doesn't contain enough information, say so and provide general guidance based on best practices.

Context:
{context}
"""
        
        # Generate response
        messages = [
            SystemMessage(content=system_msg),
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
