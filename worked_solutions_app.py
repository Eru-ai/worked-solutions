"""
NCEA Worked Solutions Explainer (v7 - ESL simpler-English toggle)
Run with: streamlit run worked_solutions_app.py
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st
from PIL import Image

MODEL_NAME = "gemini-2.5-flash-lite"

st.set_page_config(page_title="NCEA Worked Solutions", page_icon="🧮", layout="centered")

st.title("🧮 NCEA Worked Solutions")
st.caption("Physics & Maths. Get a solution, check an answer, or check your own working.")
with st.expander("ℹ️ How to use"):
    st.markdown(
        """
**Pick a mode:**
- **📖 Explain it to me** — full step-by-step solution with reasoning. For learning.
- **⚡ Just the answer** — quick answer + method. For checking work you've done.
- **✏️ Check my working** — paste or photo your attempt, find out where you went wrong.

**Tips:**
- Photos work best in good light, problem clearly visible.
- In *Check my working*, the problem is optional — skip it if your working speaks for itself.
- Tick **Explain in simpler English** if English isn't your first language.
        """
    )
# --- API key ---
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("No GEMINI_API_KEY found.")
    st.stop()
genai.configure(api_key=api_key)


def read_image(f):
    return Image.open(f)


# --- Mode first (drives what you see) ---
mode = st.radio(
    "What do you need?",
    [
        "📖 Explain it to me",
        "⚡ Just the answer",
        "✏️ Check my working",
    ],
    horizontal=True,
)
is_check = mode.startswith("✏️")

st.divider()

# --- The problem ---
if is_check:
    st.subheader("The problem *(optional)*")
    st.caption("Skip this if your working shows enough on its own.")
else:
    st.subheader("The problem")

problem_image = st.file_uploader("📷 Photo of the problem", type=["jpg", "jpeg", "png"], key="prob_img")
if problem_image:
    st.image(read_image(problem_image), width=350)

problem_text = st.text_area(
    "Or type it out",
    height=120,
    key="prob_text",
    placeholder="e.g. A 0.50 kg ball is dropped from 12 m. Find its speed just before it lands.",
    label_visibility="collapsed" if problem_image else "visible",
)

# --- Your working (check mode only) ---
student_working = ""
if is_check:
    st.subheader("Your working")
    working_image = st.file_uploader("📷 Photo of your working", type=["jpg", "jpeg", "png"], key="work_img")
    if working_image:
        st.image(read_image(working_image), width=350)

    student_working = st.text_area(
        "Or type it out",
        height=180,
        key="work_text",
        placeholder="Step 1: I used v = u + at\nStep 2: ...\nMy answer: ...",
        label_visibility="collapsed" if working_image else "visible",
    )
else:
    working_image = None

# --- Simpler English (ESL) toggle — visible so students who need it can find it ---
simpler_english = st.checkbox("🌏 Explain in simpler English (for English as a second language)")

# --- Optional context, tucked away ---
with st.expander("Add context (optional)"):
    context = st.text_input(
        "Your level or topic",
        placeholder="e.g. NCEA Level 2 Physics, mechanics",
        label_visibility="collapsed",
    )

st.divider()

# --- Go ---
if st.button("Go", type="primary", use_container_width=True):
    has_problem = bool(problem_image or problem_text.strip())
    has_working = bool(working_image or student_working.strip())

    if is_check and not has_working:
        st.warning("Add your working — a photo or typed out.")
    elif not is_check and not has_problem:
        st.warning("Add the problem — a photo or typed out.")
    else:
        images = []
        if problem_image:
            images.append(read_image(problem_image))
        if is_check and working_image:
            images.append(read_image(working_image))

        ctx = f"\nCONTEXT: {context}\n" if context.strip() else ""

        # ESL instruction — simplify LANGUAGE, never the physics/maths
        esl = (
            "\nLANGUAGE: Write for a student who is still learning English. "
            "Use very simple English, like you are explaining to someone new to the language. "
            "Rules: keep sentences short (about 10 words or less). "
            "Use easy, common words. Avoid idioms, slang, and long words where a short word works. "
            "Explain every technical term in plain words the first time you use it. "
            "Keep the physics and maths fully correct — make the WORDS simpler, not the content.\n"
            if simpler_english else ""
        )

        # Describe what's been given
        if is_check:
            parts = []
            if problem_image:
                parts.append("The problem is in the first attached image.")
            elif problem_text.strip():
                parts.append(f"THE PROBLEM:\n{problem_text}")
            else:
                parts.append("No problem statement was given — work out what the problem is from the student's working.")

            if working_image:
                parts.append("The student's working is in the last attached image.")
            else:
                parts.append(f"STUDENT'S WORKING:\n{student_working}")
            given = "\n\n".join(parts)
        else:
            given = "The problem is in the attached image." if problem_image else f"THE PROBLEM:\n{problem_text}"

        # --- Prompts ---
        if is_check:
            prompt = f"""You are an experienced NCEA Level 2/3 Physics and Maths tutor in New Zealand.

A student has attempted a problem. Check their working: what's right, where it first went wrong, and how to fix it.

Solve it yourself first, then compare. Focus on the FIRST point where they went wrong — everything after may just be a knock-on effect.

Use EXACTLY these four sections:

## ✅ What you got right
## ⚠️ Where you went wrong
(Quote their line. Explain WHY it's wrong.)
## 🔧 What to fix
## 📘 The correct working

FORMATTING: plain text maths only. No LaTeX. Use Unicode (² ³ √ × ÷ θ Δ π ≈ ±).
Refer to the student as "you". Be honest but not harsh.
{esl}
{given}
{ctx}"""
        elif mode.startswith("⚡"):
            prompt = f"""You are an experienced NCEA Level 2/3 Physics and Maths tutor in New Zealand.

The student just wants to check their answer. Be brief.

## Final Answer
(Correct units and sig figs. Bold the number. Cover all parts if multi-part.)

## Method
(1-3 sentences. Key equation only, no full working.)

FORMATTING: plain text maths only. No LaTeX. Use Unicode (² ³ √ × ÷ θ Δ π ≈ ±).
{esl}
{given}
{ctx}"""
        else:
            prompt = f"""You are an experienced NCEA Level 2/3 Physics and Maths tutor in New Zealand.

Walk the student through the solution — not just the steps, but WHY each step.

Use EXACTLY these five sections:

## Problem Setup
(Type of problem, knowns, what's needed, relevant formula.)

## Step-by-Step Solution
(Number each step. ONE action per step — never combine two actions into one step.
Keep each step to 1-2 short sentences: what you do, the working, then why.
A student should be able to follow one line at a time without freezing.
Use the ACTUAL numbers from THIS problem, not general advice.)

## Final Answer
(Correct units and sig figs. Bold the number.)

## Common Pitfalls
(1-2 mistakes students make here.)

## Key Takeaway
(One sentence.)

FORMATTING: plain text maths only. No LaTeX. Use Unicode (² ³ √ × ÷ θ Δ π ≈ ±).
Refer to the student as "you".
{esl}
{given}
{ctx}"""

        with st.spinner("Working on it..."):
            model = genai.GenerativeModel(MODEL_NAME)
            response = model.generate_content([prompt] + images if images else prompt)

        st.divider()
        st.markdown(response.text)
        st.download_button("📥 Download", data=response.text, file_name="worked_solution.txt", mime="text/plain")

st.divider()
st.caption("Found a bug or have feedback? Email me: your@email.com")