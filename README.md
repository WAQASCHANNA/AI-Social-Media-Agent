# 🤖 AI Social Media Agent

**Challenge 12: Hack-Nation 2026**

An intelligent social media content generation system that learns your brand voice, creates platform-optimized posts, and provides an agentic self-feedback loop for quality assurance.

---

## 🌟 Features

### 1. **Brand Voice Learning**
- Analyzes 2-3 sample posts to extract:
  - **Tone** (Energetic, Professional, Technical)
  - **Keywords** (most frequent terms)
  - **Visual Style** (color palette and fonts inferred from tone)

### 2. **Smart Content Generation**
- Creates **3 unique post variations** for any topic
- **Platform-specific optimization**:
  - **LinkedIn**: Professional tone, 1-3 hashtags, authoritative language
  - **Instagram**: Visual-first, 5-10 hashtags, "Link in bio" CTAs
- Generates separate **overlay text** for images (max 5 words)

### 3. **Dynamic Visual Engine**
- Renders text overlays on base images using:
  - Brand-specific colors (extracted from tone)
  - Monospace/Sans-serif fonts (based on brand voice)
  - Automatic text wrapping and centering
- Outputs ready-to-post images

### 4. **Agentic Self-Feedback Loop**
- **Critique Agent**: Scores posts (1-10) on brand alignment
- **Improvement Agent**: Rewrites captions based on critique feedback
- Iterative refinement until quality threshold is met

### 5. **Human-in-the-Loop Workflow**
- Manual editing of captions and overlay text
- Live preview of final images
- One-click download and copy-to-clipboard

### 6. **Optional AI Integration**
- Supports **Google Gemini API** for real LLM-powered generation
- Falls back to enhanced **Mock Generator** (free, fast, reliable)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/WAQASCHANNA/AI-Social-Media-Agent.git
cd AI-Social-Media-Agent
```

2. **Create virtual environment**
```bash
python -m venv venv
```

3. **Activate virtual environment**
- **Windows**:
  ```bash
  venv\Scripts\activate
  ```
- **Mac/Linux**:
  ```bash
  source venv/bin/activate
  ```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Run the application**
```bash
streamlit run app.py
```
Or simply double-click `run.bat` (Windows only).

6. **Open in browser**
Navigate to: `http://localhost:8501`

---

## 📖 Usage Guide

### Step 1: Teach the Agent Your Brand
1. Navigate to **"Setup Brand"** in the sidebar
2. Paste 2-3 examples of your best-performing posts
3. Click **"Analyze Brand Voice"**
4. Review the extracted tone, keywords, and visual style

### Step 2: Generate Content
1. Go to **"Generate Content"**
2. Select a **template** (Announcement, Product Launch, Meme, etc.)
3. Choose **platform** (LinkedIn or Instagram)
4. Enter your **intent** (e.g., "Announce our new AI feature")
5. Click **"Generate Options"**
6. Review 3 AI-generated post variations with images

### Step 3: Critique & Refine (Optional)
1. Click **"Critique"** under any post option
2. Review the AI's score and feedback
3. Click **"Apply Fix"** to auto-improve the caption
4. Repeat until satisfied

### Step 4: Review & Polish
1. Navigate to **"Review & Polish"**
2. Select your favorite post
3. Edit the overlay text and caption
4. Preview the final image
5. Click **"Download Final Image"**
6. Copy the caption to your clipboard

---

## 🏗️ Architecture

### Core Modules

| Module | Purpose |
|--------|---------|
| `app.py` | Main Streamlit application and UI |
| `brand_voice.py` | Brand voice extraction and visual style inference |
| `generator.py` | Content generation (Mock + Gemini API) |
| `critic.py` | Post critique and improvement agents |
| `visual_engine.py` | Dynamic image rendering with text overlays |
| `templates.json` | Post template definitions |
| `create_assets.py` | Asset generation script |

### Data Flow
```
User Input (Sample Posts)
    ↓
Brand Voice Extraction
    ↓
Content Generation (3 variants)
    ↓
Visual Engine (Image + Overlay)
    ↓
Critique Agent (Score + Feedback)
    ↓
Improvement Agent (Rewrite)
    ↓
Human Review & Export
```

---

## 🎨 Templates

- **Announcement**: Breaking news, product launches
- **Product Launch**: Feature highlights, benefits
- **Meme**: Humorous, relatable content
- **Data Visualization**: Stats, infographics
- **Quote**: Inspirational, thought leadership
- **Behind the Scenes**: Team culture, process

---

## 🧠 AI Integration (Optional)

### Using Google Gemini API

1. Get a free API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. In the sidebar, enter your **Gemini API Key**
3. The app will use real AI for:
   - Creative caption generation
   - Smart critique feedback
   - Context-aware improvements

### Mock Generator (Default)

If no API key is provided, the app uses an enhanced Mock Generator:
- ✅ Fast and reliable
- ✅ Platform-aware templates
- ✅ Smart text processing (strips instruction prefixes)
- ✅ Professional output

---

## 📦 Dependencies

```
streamlit==1.31.0
Pillow==10.2.0
google-generativeai==0.8.6
```

See `requirements.txt` for full list.

---

## 🎯 Hackathon Highlights

### Innovation
- **Agentic workflow**: Self-critique and improvement loop
- **Visual intelligence**: Automatic color/font inference from tone
- **Platform awareness**: LinkedIn vs Instagram optimization

### Technical Excellence
- **Modular architecture**: Separation of concerns
- **Dual-mode operation**: Mock + Real AI
- **Error handling**: Graceful fallbacks

### User Experience
- **3-step workflow**: Learn → Generate → Polish
- **Live preview**: Real-time image rendering
- **One-click export**: Download + Copy

---

## 🛠️ Development

### Project Structure
```
AI-Social-Media-Agent/
├── app.py                  # Main application
├── brand_voice.py          # Brand analysis
├── generator.py            # Content generation
├── critic.py               # Critique & improvement
├── visual_engine.py        # Image rendering
├── templates.json          # Post templates
├── requirements.txt        # Dependencies
├── run.bat                 # Windows launcher
├── assets/                 # Image assets
│   ├── product_shot.png
│   ├── gradient_bg.png
│   └── ...
└── README.md
```

### Adding New Templates

Edit `templates.json`:
```json
{
  "name": "Your Template",
  "description": "Template description",
  "base_image": "assets/your_image.png"
}
```

---

## 🤝 Contributing

This project was built for Hack-Nation 2026 Challenge 12. Feel free to fork and extend!

---

## 📄 License

MIT License - See LICENSE file for details

---

## 👨‍💻 Author

**Waqas Channa**
- GitHub: [@WAQASCHANNA](https://github.com/WAQASCHANNA)
- Challenge: Hack-Nation 2026 - Challenge 12

---

## 🙏 Acknowledgments

- Hack-Nation organizers for the challenge
- Google Gemini API for AI capabilities
- Streamlit for the amazing framework

---

**Built with ❤️ for Hack-Nation 2026**
