import streamlit as st
import json
import os
from brand_voice import extract_brand_voice
from generator import generate_captions
from critic import critique_post, improve_post
from visual_engine import create_social_post
import io

# Page Config
st.set_page_config(page_title="AI Social Media Agent", page_icon="🐦", layout="wide")

# Session State Initialization
if 'brand_profile' not in st.session_state:
    st.session_state['brand_profile'] = None
if 'generated_posts' not in st.session_state:
    st.session_state['generated_posts'] = []

# Sidebar Navigation
with st.sidebar:
    st.title("AI Social Agent 🤖")
    st.markdown("---")
    
    # API Key Input
    api_key = st.text_input("Gemini API Key (Optional)", type="password", help="Leave empty to use the free Mock Generator.")
    if api_key:
        os.environ["GEMINI_API_KEY"] = api_key
        st.success("Gemini AI Activated! 🌟")
    else:
        # Clear the environment variable if the field is empty
        if "GEMINI_API_KEY" in os.environ:
            del os.environ["GEMINI_API_KEY"]
    
    st.markdown("---")
    page = st.radio("Navigation", ["Setup Brand", "Generate Content", "Review & Polish"])
    st.markdown("---")
    st.caption("Hack-Nation Challenge 12")

# --- Page 1: Setup Brand ---
if page == "Setup Brand":
    st.header("Step 1: Teach the Agent Your Brand")
    
    st.markdown("Paste 2-3 examples of your best performing posts to help the agent learn your voice.")
    
    col1, col2 = st.columns(2)
    with col1:
        post1 = st.text_area("Example Post 1", height=100, placeholder="Excited to announce our new feature! #tech")
        post2 = st.text_area("Example Post 2", height=100, placeholder="Join us this weekend for the hackathon.")
    with col2:
        post3 = st.text_area("Example Post 3", height=100, placeholder="Did you know? optimization is key.")
        
    if st.button("Analyze Brand Voice"):
        samples = [p for p in [post1, post2, post3] if p.strip()]
        if samples:
            profile = extract_brand_voice(samples)
            st.session_state['brand_profile'] = profile
            st.success("Brand Voice Analyzed!")
            st.json(profile)
        else:
            st.warning("Please enter at least one example post.")

# Imports moved to top


# --- Page 2: Generate Content ---
elif page == "Generate Content":
    st.header("Step 2: Generate New Posts")
    
    if not st.session_state['brand_profile']:
        st.warning("Please set up your brand voice in Step 1 first.")
    else:
        profile = st.session_state['brand_profile']
        
        # Display Brand Identity
        col_brand1, col_brand2 = st.columns([1, 3])
        with col_brand1:
            st.color_picker("Brand Color", profile['visual_style']['color'], disabled=True)
        with col_brand2:
            st.info(f"**Voice:** {profile['tone']} | **Font:** {profile['visual_style']['font']} | **Keywords:** {', '.join(profile['keywords'])}")
        
        col_input1, col_input2 = st.columns(2)
        with col_input1:
            # Load Templates
            try:
                with open('templates.json', 'r') as f:
                    templates = json.load(f)
                template_names = [t['name'] for t in templates]
                selected_template_name = st.selectbox("Choose a Template", template_names)
                selected_template = next(t for t in templates if t['name'] == selected_template_name)
            except FileNotFoundError:
                st.error("templates.json not found.")
                st.stop()
        
        with col_input2:
            platform = st.radio("Target Platform", ["LinkedIn", "Instagram"], horizontal=True)

        intent = st.text_input("What is this post about?", placeholder="e.g. Announcing the Hack-Nation winners")
        
        if st.button("Generate Options"):
            with st.spinner("Generating creative options..."):
                captions = generate_captions(profile, intent, selected_template, platform, n=3)
                st.session_state['generated_posts'] = captions
                st.success("Generated 3 options!")

        if st.session_state['generated_posts']:
            st.subheader("Draft Options")
            for i, post in enumerate(st.session_state['generated_posts']):
                with st.container():
                    st.markdown(f"**Option {i+1}**")
                    


                    # Display the structured post
                    c1, c2 = st.columns([1, 2])
                    with c1:
                        # Render Image
                        base_image = "assets/product_shot.png" # Default fallback, should use template data
                        # Find the template image from the selected template object if possible, or use a default
                        if 'default_image' in selected_template:
                             base_image = selected_template['default_image']
                        
                        generated_img = create_social_post(base_image, post['overlay'], profile['visual_style'])
                        st.image(generated_img, caption=f"Style: {post.get('image_style', 'Standard')}", use_column_width=True)
                        
                        # Download Button
                        buf = io.BytesIO()
                        generated_img.save(buf, format="PNG")
                        byte_im = buf.getvalue()
                        st.download_button(
                            label=f"Download Image {i+1}",
                            data=byte_im,
                            file_name=f"social_post_{i+1}.png",
                            mime="image/png"
                        )

                    with c2:
                         st.text_area("Caption", post['caption'], height=150, key=f"cap_{i}")
                    
                    
                    col_a, col_b = st.columns([1, 4])
                    with col_a:
                        if st.button(f"Critique {i+1}", key=f"crit_{i}"):
                            # Pass just the caption for now, expand later
                            critique = critique_post(post['caption'], profile)
                            st.write(f"**Score:** {critique['score']}/10")
                            st.caption(f"Feedback: {critique['feedback']}")
                            st.session_state[f'critique_{i}'] = critique
                    
                    if f'critique_{i}' in st.session_state:
                         if st.button(f"Apply Fix {i+1}", key=f"imp_{i}"):
                             improved = improve_post(post['caption'], st.session_state[f'critique_{i}']['feedback'])
                             st.session_state['generated_posts'][i]['caption'] = improved
                             st.rerun()




# --- Page 3: Review & Polish ---
elif page == "Review & Polish":
    st.header("Step 3: Human Review & Polish")
    st.markdown("Refine your selected post and export the final version.")
    
    if not st.session_state['generated_posts']:
        st.warning("No posts generated yet. Go to 'Generate Content' first.")
    else:
        # Select which post to polish
        st.subheader("Select a Post to Polish")
        post_options = [f"Option {i+1}" for i in range(len(st.session_state['generated_posts']))]
        selected_idx = st.selectbox("Choose your favorite", range(len(post_options)), format_func=lambda x: post_options[x])
        
        selected_post = st.session_state['generated_posts'][selected_idx]
        
        st.markdown("---")
        st.subheader("Edit & Refine")
        
        col_edit1, col_edit2 = st.columns([1, 2])
        
        with col_edit1:
            st.markdown("**Image Overlay Text**")
            overlay_text = st.text_input("Overlay", value=selected_post['overlay'], key="overlay_edit")
            
            st.markdown("**Preview**")
            # Generate preview image
            profile = st.session_state.get('brand_profile', {})
            base_image = "assets/product_shot.png"
            
            preview_img = create_social_post(base_image, overlay_text, profile.get('visual_style', {}))
            st.image(preview_img, use_column_width=True)
            
            # Download button
            buf = io.BytesIO()
            preview_img.save(buf, format="PNG")
            byte_im = buf.getvalue()
            st.download_button(
                label="📥 Download Final Image",
                data=byte_im,
                file_name="final_social_post.png",
                mime="image/png",
                type="primary"
            )
        
        with col_edit2:
            st.markdown("**Caption Text**")
            caption_text = st.text_area("Caption", value=selected_post['caption'], height=200, key="caption_edit")
            
            st.markdown("**Character Count**")
            st.caption(f"{len(caption_text)} characters")
            
            st.markdown("**Copy to Clipboard**")
            st.code(caption_text, language=None)
            st.caption("👆 Click to select, then Ctrl+C to copy")


