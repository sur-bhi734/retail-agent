from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

with open("prompts/system_prompt.txt") as f:
    SYSTEM_PROMPT = f.read()

def build_prompt(profile, events, top_products, trends=None, peer_data=None) -> str:
    events_str = ", ".join([e["name"] for e in events]) if events else "None"
    top_str = ", ".join([p.get("name", "") for p in top_products])

    # Scoring factors — give the LLM the actual reasons each product was chosen
    score_factors = []
    if profile.get("style_pref"):
        score_factors.append(f"style match ({profile['style_pref']})")
    if profile.get("budget"):
        score_factors.append(f"budget fit ({profile['budget']})")
    if profile.get("color_pref"):
        score_factors.append(f"color preference ({profile['color_pref']})")
    if events:
        score_factors.append(f"event relevance ({events_str})")
    if peer_data and peer_data.get("peer_categories"):
        score_factors.append(f"peer influence ({', '.join(peer_data['peer_categories'][:2])})")
    if trends and trends.get("top_colors"):
        score_factors.append(f"local color trends ({', '.join(trends['top_colors'][:2])})")

    factors_str = ", ".join(score_factors) if score_factors else "profile fit"

    school_trend_str = ""
    if trends and trends.get("school_trends") and profile.get("school"):
        school_names = [t.get("product_name", "") for t in trends["school_trends"][:2]]
        if school_names:
            school_trend_str = f"\nSchool Trends ({profile['school']}): {', '.join(school_names)}"

    return f"""
SHOPPER PROFILE
---------------
Name: {profile.get('name')}
Style Preference: {profile.get('style_pref')}
Color Preference: {profile.get('color_pref')}
Budget: {profile.get('budget')}
Occasion: {profile.get('occasion', 'General')}

CONTEXT
-------
Upcoming Events: {events_str}
Top Recommended Products: {top_str}{school_trend_str}

SCORING FACTORS (explain these in your reasoning)
--------------------------------------------------
The recommendations above were chosen based on: {factors_str}.
Please explain in your narrative why each of these factors makes the recommended items a good fit for this shopper.
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