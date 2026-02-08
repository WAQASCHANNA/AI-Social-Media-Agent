import random
import time
import os
import json
try:
    import google.generativeai as genai
except ImportError:
    genai = None

def generate_captions(brand_profile, intent, template_name, platform="LinkedIn", n=3):
    """
    Generates captions using OpenAI if key is present, else uses Mock.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key and genai:
        return generate_captions_with_llm(api_key, brand_profile, intent, template_name, platform, n)
    
    # Mock LLM generation. 
    # Simulate API latency
    time.sleep(1.0)
    
    tone = brand_profile.get('tone', 'Neutral')
    keywords = brand_profile.get('keywords', [])
    keywords_str = ", ".join(keywords[:2])
    
    captions = []
    
    # Platform nuancing
    emoji_limit = 5 if platform == "Instagram" else 1
    hashtag_limit = 10 if platform == "Instagram" else 3
    length_desc = "short and punchy" if platform == "Instagram" else "professional and detailed"

    base_overlay = f"{intent.upper()}"
    
    # Cleaning intent for better overlay
    clean_intent = intent
    prefixes = ["Announce that ", "Promote ", "Share that "]
    for p in prefixes:
        if clean_intent.lower().startswith(p.lower()):
            clean_intent = clean_intent[len(p):]
            break
            
    # Shorten for overlay
    if len(clean_intent) > 30:
        clean_intent = clean_intent[:27] + "..."
    
    patterns = {
        "Energetic": [
            {
                "caption": f"🚀 {clean_intent}! We are so hyped to share this. #{keywords_str} #HackNation",
                "overlay": f"HYPE: {clean_intent.upper()}!"
            },
            {
                "caption": f"Boom! 💥 {clean_intent}. Don't miss out! Check the link in bio. 🔗",
                "overlay": f"DON'T MISS: {clean_intent}"
            }
        ],
        "Professional": [
            {
                "caption": f"We are pleased to announce {clean_intent}. Consistency is key to our strategy. #{keywords_str}",
                "overlay": f"ANNOUNCING: {clean_intent}"
            },
            {
                "caption": f"Strategic Update: {clean_intent}. Leveraging our core strengths to deliver value.",
                "overlay": f"KEY UPDATE: {clean_intent}"
            }
        ],
        "Technical": [
            {
                "caption": f"git commit -m '{clean_intent}'. v2.0 optimized and ready to deploy. 💻 #{keywords_str}",
                "overlay": f"> {clean_intent}"
            },
            {
                "caption": f"System upgrade: {clean_intent}. Latency reduced by 50%. Read the docs.",
                "overlay": f"SYSTEM: {clean_intent.upper()}"
            }
        ]
    }
    
    base_patterns = patterns.get(tone, patterns["Professional"])
    
    for i in range(n):
        if i < len(base_patterns):
            # Customize based on platform (simple mock modification)
            caption_text = base_patterns[i]["caption"]
            if platform == "Instagram" and "Link in bio" not in caption_text:
                caption_text += " 🔗 Link in bio!"
            elif platform == "LinkedIn":
                caption_text = caption_text.replace("Link in bio", "").strip()
                
            captions.append({
                "caption": caption_text,
                "overlay": base_patterns[i]["overlay"],
                "image_style": brand_profile.get("visual_style", {}).get("color", "gray")
            })
        else:
            captions.append({
                "caption": f"{intent} - Variant {i+1} ({tone} style) for {platform}",
                "overlay": f"{intent} ({i+1})",
                "image_style": "Generic"
            })
            
    return captions

def generate_captions_with_llm(api_key, brand_profile, intent, template_name, platform, n=3):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.0-pro')
    
    tone = brand_profile.get('tone', 'Neutral')
    # Handle list or string for keywords safely
    k_list = brand_profile.get('keywords', [])
    if isinstance(k_list, list):
        keywords = ", ".join(k_list)
    else:
        keywords = str(k_list)
        
    visual_style = brand_profile.get('visual_style', {}).get('color', 'gray')

    prompt = f"""
    You are a social media manager.
    Brand Tone: {tone}
    Keywords: {keywords}
    
    Task: Create {n} distinct posts about "{intent}" for {platform}.
    Template: {template_name}
    
    Constraints:
    - LinkedIn: Professional, 1-3 hashtags.
    - Instagram: Visual, 5-10 hashtags, "Link in bio".
    
    Output strictly valid JSON array like this:
    [
      {{
        "caption": "Post text...",
        "overlay": "Image text (max 5 words)",
        "image_style": "{visual_style}"
      }}
    ]
    """

    try:
        response = model.generate_content(prompt)
        text = response.text
        # Clean markdown if present
        text = text.replace("```json", "").replace("```", "").strip()
        
        data = json.loads(text)
        
        # Handle if wrapped in dict or list
        if isinstance(data, list):
            return data
        if isinstance(data, dict) and "posts" in data:
            return data["posts"]
            
        return []
    except Exception as e:
        print(f"Gemini Error: {e}")
        import streamlit as st
        st.error(f"Gemini Error: {e}")
        return []
