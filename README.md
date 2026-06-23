# 🧮 NCEA Worked Solutions Explainer

> AI tool that reads a Physics or Maths problem (from a photo or text), walks you through a step-by-step worked solution, and explains *why* each step works.

🚀 **[Live demo](https://ncea-worked-solutions.streamlit.app/)** — try it now

<img width="869" height="386" alt="image" src="https://github.com/user-attachments/assets/766d8b07-ffaf-48f7-be53-3230022c2ca6" />


## What it does

Stuck on a Physics or Maths problem? Snap a photo (textbook, notes, whiteboard) or paste the text. The tool sends it to Google's Gemini AI — which has **vision capability**, meaning it can read images directly — and returns either:

- **Full explanation mode** — Problem Setup, Step-by-Step Solution, Final Answer, Common Pitfalls, Key Takeaway. For when you actually want to *learn* the topic.
- **Quick check mode** — just the Final Answer + a 1-3 sentence method. For when you've done the work and want to verify.

Designed for NCEA Levels 1–3, primarily Physics and Maths.

## How to use

1. Open the [live app](https://ncea-worked-solutions.streamlit.app/)
2. Upload a photo of your problem **or** paste the text
3. (Optional) Add context — your NCEA level, the topic, anything that helps
4. Choose **Full explanation** or **Quick check**
5. Hit **Get Worked Solution**

## Tech stack

- **Python** — core language
- **Streamlit** — web UI
- **Google Gemini API** (`gemini-2.5-flash-lite`) — AI engine with vision support
- **Pillow (PIL)** — image handling for photo uploads
- **python-dotenv** — secret management

## Run it yourself

```bash
git clone https://github.com/Eru-ai/worked-solutions.git
cd worked-solutions
python -m venv .venv
.\.venv\Scripts\Activate.ps1     # Windows
# source .venv/bin/activate       # Mac/Linux
pip install -r requirements.txt
echo "GEMINI_API_KEY=your_key_here" > .env
streamlit run worked_solutions_app.py
```

Get a free Gemini API key from [aistudio.google.com](https://aistudio.google.com).

## About

Built by [Eru Kawakami](https://github.com/Eru-ai), 16, NCEA Level 2 student in New Zealand. Third deployed AI tool — first one with image input.

Follow the journey: [@erukawa_ai](https://x.com/erukawa_ai)<img width="869" height="380" alt="Screenshot 2026-06-23 212004" src="https://github.com/user-attachments/assets/d3f680d0-2035-40cd-82e8-1e4e41f8256e" />
