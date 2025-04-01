# Step1: Setup API Keys for Groq and Tavily (No OpenAI)
import os

# Set API Keys Directly
TAVILY_API_KEY = "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"
GROQ_API_KEY = "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"

# Ensure environment variables are set correctly
os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# Step2: Setup LLM (Groq) & Search Tool (Tavily)
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults

# Initialize Groq LLM
groq_llm = ChatGroq(model="llama-3.3-70b-versatile")

# Initialize Tavily Search Tool
search_tool = TavilySearchResults(max_results=2)

# Step3: Setup AI Agent with Search tool functionality
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage

# System Prompt
system_prompt = "Act as an AI chatbot who is smart and friendly."

def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt):
    """
    This function invokes the AI agent with the given model, query, and optional search capability.
    """
    llm = ChatGroq(model=llm_id)  # Always use Groq (No OpenAI)

    # Add search tool only if search is allowed
    tools = [search_tool] if allow_search else []
    
    # Create AI agent
    agent = create_react_agent(
        model=llm,
        tools=tools,
        state_modifier=system_prompt
    )
    
    # Define input state
    state = {"messages": query}
    
    # Invoke AI agent
    response = agent.invoke(state)
    
    # Extract AI messages
    messages = response.get("messages", [])
    ai_messages = [msg.content for msg in messages if isinstance(msg, AIMessage)]
    
    return ai_messages[-1] if ai_messages else "No response generated."
