import streamlit as st

AUDIENCE_OPTIONS = [
    "Student",
    "Professional",
    "Executive",
    "Teacher",
    "Child"
]

TONE_OPTIONS = [
    "Formal",
    "Casual",
    "Friendly",
    "Persuasive",
    "Professional"
]


def render_sidebar():

    st.sidebar.markdown("""
    <h2 style="
        color:white;
        margin-bottom:8px;
        font-weight:700;
    ">
    ⚙ Controls
    </h2>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("""
    <div style="
        background:#1E293B;
        padding:18px;
        border-radius:18px;
        border:1px solid rgba(255,255,255,.08);
        margin-bottom:20px;
    ">

    <h4 style="
        color:white;
        margin:0;
    ">
    ✨ Audience-Aware Rewriter
    </h4>

    <p style="
        color:#CBD5E1;
        margin-top:8px;
        font-size:14px;
        line-height:1.6;
    ">
    Rewrite text using Groq AI,
    analyze readability,
    export in multiple formats
    and generate voice.
    </p>

    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("### 🎯 Audience")

    audience = st.sidebar.selectbox(
        "",
        AUDIENCE_OPTIONS,
        index=1
    )

    st.sidebar.markdown("### 💬 Tone")

    tone = st.sidebar.selectbox(
        "",
        TONE_OPTIONS,
        index=0
    )

    st.sidebar.markdown("---")

    st.sidebar.markdown("### 🎚 Adjustments")

    length = st.sidebar.slider(
        "Length",
        0,
        2000,
        400,
        50
    )

    formality = st.sidebar.slider(
        "Formality",
        0,
        100,
        60,
        5
    )

    sliders = {
        "length": length,
        "formality": formality,
    }

    return audience, tone, sliders