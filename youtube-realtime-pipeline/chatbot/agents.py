from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.prompts import ChatPromptTemplate
import os

def create_youtube_agent(tools):
    """Create LangChain agent with Google ADK"""
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful AI assistant analyzing YouTube video metadata.
        You have access to a database containing video information from high-frequency channels.
        Use the provided tools to query the database and answer user questions accurately."""),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ])
    
    agent = create_tool_calling_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)
