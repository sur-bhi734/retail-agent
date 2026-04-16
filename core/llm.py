from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

with open("prompts/system_prompt.txt") as f:
    SYSTEM_PROMPT = f.read()

def build_prompt(profile, events, top_products) -> str:
    events_str = ", ".join([e["name"] for e in events]) if events else "None"
    top_str = ", ".join([p.get("name", "") for p in top_products])
    
    return f"""
SHOPPER PROFILE
---------------
Name: {profile.get('name')}
Style Preference: {profile.get('style_pref')}
Color Preference: {profile.get('color_pref')}

CONTEXT
-------
Upcoming Events: {events_str}
Top Recommended Products: {top_str}
"""

def call_llm(prompt: str) -> str:
    """Calls Ollama using LangChain, returns only the narrative string"""
    try:
        llm = ChatOllama(model="gemma:2b")
        
        chat_prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("user", "{input_prompt}")
        ])
        
        chain = chat_prompt | llm | StrOutputParser()
        
        return chain.invoke({"input_prompt": prompt}).strip()
    except Exception:
        return "AI reasoning temporarily unavailable."
