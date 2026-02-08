import re
from collections import Counter
import streamlit as st

@st.cache_data
def extract_brand_voice(sample_posts):
    """
    Analyzes list of sample posts and returns a dictionary of brand voice attributes.
    In a real scenario, this would use an LLM or more advanced NLP.
    For this prototype, we use simple keyword frequency and length analysis.
    """
    if not sample_posts:
        return {"tone": "Neutral", "keywords": []}

    all_text = " ".join(sample_posts).lower()
    words = re.findall(r'\w+', all_text)
    
    # Filter common stop words (very basic list)
    stop_words = set(['the', 'a', 'an', 'and', 'is', 'to', 'in', 'of', 'for', 'with', 'on', 'at', 'by', 'from'])
    filtered_words = [w for w in words if w not in stop_words and len(w) > 3]
    
    # Get most common keywords
    keyword_counts = Counter(filtered_words)
    top_keywords = [word for word, count in keyword_counts.most_common(5)]
    
    # Determine tone based on simple heuristics
    tone = "Professional"
    visual_style = {"color": "#0077B5", "font": "Sans-Serif"} # Default LinkedIn Blue

    if "!" in all_text:
        tone = "Energetic"
        visual_style = {"color": "#FF5733", "font": "Modern Bold"} # Orange
    if "help" in all_text or "support" in all_text:
        tone = "Helpful"
        visual_style = {"color": "#28A745", "font": "Friendly/Rounded"} # Green
    if "code" in all_text or "hack" in all_text or "api" in all_text:
        tone = "Technical"
        visual_style = {"color": "#61DAFB", "font": "Monospace"} # React Blue/Tech

    return {
        "tone": tone,
        "keywords": top_keywords,
        "visual_style": visual_style,
        "avg_length": sum(len(p.split()) for p in sample_posts) / len(sample_posts)
    }
