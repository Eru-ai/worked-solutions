"""
NCEA Worked Solutions Explainer (v3)
- Image OR text input
- Toggle: Full explanation (learning) vs Quick check (just the answer)

Run with: streamlit run worked_solutions_app.py
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st
from PIL import Image

# --- Config ---
MODEL_NAME = "gemini-2.5-flash-lite"

# --- Page setup ---
st.set_page_config(
    page_title="NCEA Worked Solutions",
    page_icon="🧮",
    layout="wide",
)

# --- Title and description ---
st.title("🧮 NCEA Worked Solutions Explainer")
st.markdown(
    "Stuck on a Physics or Maths problem? **Snap a photo or paste the problem below** — "
    "get a worked solution **explained like a tutor would**, or a quick answer check."
)

with st.expander("ℹ️  How to use this tool"):
    st.markdown(
        """
**Steps:**
1. **Provide your problem** — upload a photo (textbook, notes, whiteboard) OR paste/type the text.
2. **(Optional) Add context** — your level (NCEA 1/2/3), topic, anything helpful.
3. **Pick a mode:**
   - **Full explanation** — step-by-step reasoning to learn from
   - **Quick check** — just the answer + method, for verifying work you've already done
4. Click **Get Worked Solution**.

**Tip:** photos work best when the problem is clearly visible — good lighting, not too small.
"""
    )

# --- API key check ---
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("No GEMINI_API_KEY found. Set it in your .env file or Streamlit secrets.")
    st.stop()
genai.configure(api_key=api_key)

# --- Input area ---
st.subheader("Your problem")

problem_image = st.file_uploader(
    "📷 Upload a photo of the problem (jpg, png)",
    type=["jpg", "jpeg", "png"],
    key="problem_image",
)

if problem_image:
    img_preview = Image.open(problem_image)
    st.image(img_preview, caption="Your uploaded problem", width=400)

problem_text = st.text_area(
    "✍️  Or paste / type the problem here",
    height=150,
    key="problem_text",
    placeholder="e.g. A 2.0 kg block slides down a frictionless ramp inclined at 30°...",
)

st.subheader("Context (optional)")
context = st.text_area(
    "Your level, topic, or anything else helpful",
    height=80,
    label_visibility="collapsed",
    placeholder="e.g. NCEA Level 2 Physics, mechanics topic",
)

# Mode toggle
mode = st.radio(
    "Mode",
    options=["Full explanation (learning)", "Quick check (just the answer)"],
    horizontal=True,
)
is_quick = mode.startswith("Quick")

# --- Generate solution ---
if st.button("Get Worked Solution", type="primary", use_container_width=True):
    if not problem_image and not problem_text.strip():
        st.warning("Please upload a photo of the problem OR paste it as text.")
    else:
        context_section = f"\nSTUDENT CONTEXT:\n{context}\n" if context.strip() else ""

        if problem_image:
            problem_section = "The student's problem is shown in the attached image. Read it carefully — if there's a diagram, briefly describe what you see."
        else:
            problem_section = f"PROBLEM:\n{problem_text}"

        if is_quick:
            prompt = f"""You are an experienced NCEA Level 2/3 Physics and Maths tutor in New Zealand.

A student needs to QUICKLY CHECK their answer to a problem — they've already done the work, they just want to verify.

Be brief. Use exactly this structure:

## Final Answer
- State the answer with correct units and significant figures
- Make the final number **bold**
- If the problem has multiple parts (a, b, c...), give each answer

## Method
- 1-3 sentences only. State the approach used.
- Show the key equation but NOT the full working.

That's all. The student is checking work, not learning from scratch.

{problem_section}
{context_section}

Now provide the quick check."""
        else:
            prompt = f"""You are an experienced NCEA Level 2/3 Physics and Maths tutor in New Zealand.

A student will give you a problem. Walk them through the solution step-by-step, the way an excellent tutor would — not just showing the steps, but explaining WHY each step is taken.

Your response must have EXACTLY these five sections, in this order, using these exact headers:

## Problem Setup
- Identify what type of problem this is (kinematics, energy, circuits, calculus, trig, etc.)
- List the known values and what you need to find
- Identify the relevant formula(s) or concept(s)

## Step-by-Step Solution
For each step:
- State what you're doing
- Show the working clearly. Plain text math is preferred (e.g. "a = g × sin(θ) = 9.8 × 0.5 = 4.9 m/s²"). Use Unicode symbols where helpful (θ Δ π ² ³ √ ° ≈) and plain operators (* for multiply, / for divide, ^ for powers, sqrt() for roots).
- Explain WHY this step

## Final Answer
- State the answer with correct units and significant figures
- Make the final number bold (use markdown ** **)

## Common Pitfalls
- 1-2 common mistakes students make on this type of problem
- How to avoid them

## Key Takeaway
- One-sentence summary of the main concept this problem tests

GUIDELINES:
- Match NCEA Level 2-3 understanding.
- Be encouraging but not patronising.
- If the problem has missing info, state what you're assuming.

{problem_section}
{context_section}

Now walk through the solution."""

        with st.spinner("Working through your problem..."):
            model = genai.GenerativeModel(MODEL_NAME)

            if problem_image:
                img = Image.open(problem_image)
                response = model.generate_content([prompt, img])
            else:
                response = model.generate_content(prompt)

        st.divider()
        st.markdown(response.text)

        st.download_button(
            label="📥 Download solution as .txt",
            data=response.text,
            file_name="worked_solution.txt",
            mime="text/plain",
        )