def generate_captions_with_llm(api_key, brand_profile, intent, template_name, platform, n=3):
    client = OpenAI(api_key=api_key)
    
    tone = brand_profile.get('tone', 'Neutral')
    keywords = ", ".join(brand_profile.get('keywords', []))
    visual_style = brand_profile.get('visual_style', {}).get('color', 'gray')

    prompt = f"""
    You are a professional social media manager for a brand with the following voice:
    - Tone: {tone}
    - Keywords: {keywords}
    
    Task: Create {n} distinct social media posts for {platform}.
    Topic/Intent: "{intent}"
    Template Context: {template_name}
    
    Constraints for {platform}:
    - LinkedIn: Professional, authoritative, 1-3 hashtags, no overlay emojis.
    - Instagram: Engaging, visual-first, 5-10 hashtags, "Link in bio" CTA.
    
    Output Format (JSON Array):
    [
        {{
            "caption": "Full post caption...",
            "overlay": "Short text for image (max 5 words)",
            "image_style": "{visual_style}"
        }}
    ]
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # or gpt-3.5-turbo if 4o-mini not available
            messages=[
                {"role": "system", "content": "You are a creative social media AI assistant that outputs strict JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        data = json.loads(response.choices[0].message.content)
        # Handle if LLM wraps in a key like "posts": [...]
        if "posts" in data:
            return data["posts"]
        return data if isinstance(data, list) else []
    except Exception as e:
        print(f"LLM Error: {e}")
        # Fallback to mock if API fails
        return []
