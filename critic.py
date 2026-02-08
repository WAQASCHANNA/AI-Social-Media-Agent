import time
import os
import json
try:
    import google.generativeai as genai
except ImportError:
    genai = None

def critique_post(post_content, brand_profile):
    """
    Evaluates the post for compliance with brand voice.
    uUses OpenAI if key is present.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key and genai:
        return critique_post_with_llm(api_key, post_content, brand_profile)

    # Mock Critic Agent.
    time.sleep(1)
    
    tone = brand_profile.get('tone', 'Neutral')
    score = 8  # Default good score
    feedback = "Looks good!"
    
    # Simple heuristic checks
    if len(post_content) < 20:
        score -= 2
        feedback = "Too short. Expand on the value proposition."
        
    if tone == "Energetic" and "!" not in post_content:
        score -= 1
        feedback = "Needs more energy! Add an exclamation or emoji."
        
    if tone == "Technical" and "#" not in post_content:
        score -= 1
        feedback = "Add relevant hashtags for visibility."

    return {
        "score": score,
        "feedback": feedback
    }

def improve_post(post_content, feedback):
    """
    Rewrites post based on feedback.
    Uses OpenAI if key is present.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key and genai:
        return improve_post_with_llm(api_key, post_content, feedback)
        
    # Mock rewriting
    return post_content + " (Improved)"

def critique_post_with_llm(api_key, post_content, brand_profile):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.0-pro')
    
    tone = brand_profile.get('tone', 'Neutral')
    
    prompt = f"""
    You are a strict Brand Compliance Officer.
    Brand Voice: {tone}
    
    Review this post:
    "{post_content}"
    
    Score it 1-10 on alignment with the brand voice and effectiveness.
    Provide 1 sentence of specific feedback for improvement.
    
    Output strictly valid JSON:
    {{
        "score": 8,
        "feedback": "Short feedback here."
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        text = response.text.replace("```json", "").replace("```", "").strip()
        data = json.loads(text)
        return data
    except:
        return {"score": 5, "feedback": "AI Error. Check connection."}

def improve_post_with_llm(api_key, post_content, feedback):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Rewrite this social media post to address the feedback.
    Original: "{post_content}"
    Feedback: "{feedback}"
    
    Output only the rewritten post text.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except:
        return post_content + " (AI Error)"
