import streamlit as st

def apply_theme():
    st.markdown("""
<style>

/* ---------------- GLOBAL ---------------- */

.stApp{
    background:#0B1120;
    color:#F8FAFC;
}

html,body{
    color:#F8FAFC;
    font-family:Inter,Segoe UI,sans-serif;
}

/* ---------------- SIDEBAR ---------------- */

section[data-testid="stSidebar"]{
    background:#111827 !important;
    border-right:1px solid rgba(255,255,255,.08);
}

/* headings */

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3{
    color:#FFFFFF !important;
}

/* labels */

section[data-testid="stSidebar"] label{
    color:#F8FAFC !important;
    font-weight:600;
}

/* paragraph */

section[data-testid="stSidebar"] p{
    color:#CBD5E1 !important;
}

/* markdown */

section[data-testid="stSidebar"] .stMarkdown{
    color:#CBD5E1 !important;
}

/* ---------------- INPUTS ---------------- */

.stTextArea textarea{
    background:#1E293B !important;
    color:white !important;
    border-radius:14px !important;
    border:1px solid #334155 !important;
}

.stTextArea textarea::placeholder{
    color:#94A3B8 !important;
}

.stTextInput input{
    background:#1E293B !important;
    color:white !important;
}

/* ---------------- SELECTBOX ---------------- */

div[data-baseweb="select"]>div{
    background:#1E293B !important;
    border-radius:12px !important;
    border:1px solid #334155 !important;
}

div[data-baseweb="select"] *{
    color:white !important;
}

/* ---------------- FILE UPLOADER ---------------- */

[data-testid="stFileUploader"]{
    background:#1E293B;
    border-radius:18px;
    border:2px dashed #475569;
    padding:10px;
}

/* ---------------- BUTTONS ---------------- */

.stButton>button{

    background:#1E293B !important;

    color:white !important;

    border:1px solid #334155 !important;

    border-radius:14px !important;

    font-weight:600;

    transition:.25s;

}

.stButton>button:hover{

    background:#2563EB !important;

    color:white !important;

}

/* ---------------- DOWNLOAD BUTTON ---------------- */

.stDownloadButton>button{

    background:#7C3AED !important;

    color:white !important;

}

/* ---------------- SLIDER ---------------- */

.stSlider label{

    color:white !important;

}

.stSlider span{

    color:#CBD5E1 !important;

}

/* ---------------- TABS ---------------- */

button[role="tab"]{

    color:#CBD5E1 !important;

}

button[aria-selected="true"]{

    color:white !important;

}

/* ---------------- SUCCESS ---------------- */

.stSuccess{

    border-radius:14px;

}

/* ---------------- INFO ---------------- */

.stInfo{

    border-radius:14px;

}
/* ---------------- LABEL COLORS ---------------- */

/* Main labels */
label{
    color:#F8FAFC !important;
    font-size:17px !important;
    font-weight:600 !important;
}

/* Text Area label */
.stTextArea label{
    color:#FFFFFF !important;
    font-size:18px !important;
    font-weight:700 !important;
}

/* File uploader label */
.stFileUploader label{
    color:#FFFFFF !important;
    font-size:18px !important;
    font-weight:700 !important;
}

/* Captions (Paste your text..., Upload PDF, etc.) */
[data-testid="stCaptionContainer"]{
    color:#CBD5E1 !important;
    font-size:15px !important;
}

/* All markdown text */
.stMarkdown{
    color:#F8FAFC !important;
}
                
</style>
""", unsafe_allow_html=True)