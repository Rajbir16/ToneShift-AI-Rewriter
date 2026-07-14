import streamlit as st
from datetime import datetime

from ui.theme import apply_theme
from ui.components import render_sidebar
from core.groq_client import GroqClient
from core.rewrite_engine import rewrite_text
from core.prompt_builder import build_prompt
from parsers.pdf_parser import parse_pdf
from parsers.docx_parser import parse_docx
from core.analysis import analyze_text
from storage.history import HistoryStore
from exporters.txt_exporter import export_txt
from exporters.docx_exporter import export_docx
from exporters.pdf_exporter import export_pdf
from audio.tts_player import text_to_speech


def main():
    st.set_page_config(
        page_title="ToneShift",
        page_icon="📝",
        layout="wide",
    )
    apply_theme()

    groq_client = GroqClient()
    history = HistoryStore()

    st.markdown("""
<div style="
background:linear-gradient(135deg,#2563EB,#7C3AED);
padding:35px;
border-radius:22px;
box-shadow:0 20px 40px rgba(0,0,0,.35);
margin-bottom:20px;
">

<h1 style="
margin:0;
font-size:42px;
font-weight:800;
color:white;">
🚀 ToneShift
</h1>

<p style="
margin-top:12px;
font-size:18px;
color:#E2E8F0;">
AI Powered Audience-Aware Rewriter using Groq AI

Rewrite • Analyze • Export • Voice
</p>

</div>
""" ,unsafe_allow_html=True,
    )

    audience, tone, sliders = render_sidebar()

    # Ensure Groq key is present; show a friendly UI message instead of crashing.
    if not groq_client.connected:
        st.sidebar.warning("Groq is not connected. Add GROQ_API_KEY in your .env (or Streamlit secrets) then click Test Connection.")

    st.markdown(
    "<h2 style='color:#FFFFFF;font-size:34px;font-weight:700;'>📥 Input</h2>",
    unsafe_allow_html=True,
)
    col1, col2 = st.columns(2)

    # Initialize session state for input text if it doesn't exist
    if "input_text" not in st.session_state:
        st.session_state["input_text"] = ""

    with col1:
        # The text area is now the single source of truth for the input text.
        # File uploads will populate this text area.
        st.session_state["input_text"] = st.text_area(
            "Paste your text or upload a file",
            height=220,
            value=st.session_state["input_text"],
            key="text_area_input"
        )

    with col2:
        pdf_file = st.file_uploader("Upload PDF", type=["pdf"], key="pdf_uploader")
        docx_file = st.file_uploader("Upload DOCX", type=["docx"], key="docx_uploader")

    # Process file uploads and update the text area in session state
    if pdf_file is not None:
        try:
            st.session_state["input_text"] = parse_pdf(pdf_file)
            st.success("PDF text extracted.")
            st.experimental_rerun() # Rerun to update the text_area with the new content
        except Exception as e:
            st.error(f"Failed to parse PDF: {e}")

    if docx_file is not None:
        try:
            st.session_state["input_text"] = parse_docx(docx_file)
            st.success("DOCX text extracted.")
            st.experimental_rerun() # Rerun to update the text_area with the new content
        except Exception as e:
            st.error(f"Failed to parse DOCX: {e}")

    length_slider = sliders["length"]
    formality_slider = sliders["formality"]

    st.markdown(
    "<h2 style='color:#FFFFFF;font-size:34px;font-weight:700;'>✍ Rewrite</h2>",
    unsafe_allow_html=True,
)
    c1, c2, c3 = st.columns([1, 1, 1])

    # Connection test
    if c1.button("Test Connection", use_container_width=True):
        status = groq_client.test_connection()
        if status.ok:
            st.success(f"🟢 Connected to Groq ({status.model})")
        else:
            st.error(f"🔴 Disconnected: {status.error}")

    target_length = int(length_slider)
    st.caption(f"Target length: {target_length}")

    if c2.button("Rewrite", type="primary", use_container_width=True):
        if not st.session_state["input_text"].strip():
            st.warning("Please paste text or upload a PDF/DOCX.")
            st.stop()

        with st.spinner("Rewriting with Groq..."):
            prompt = build_prompt(
                text=st.session_state["input_text"],
                audience=audience,
                tone=tone,
                target_length=target_length,
                formality=formality_slider,
            )
            rewritten = rewrite_text(groq_client, prompt=prompt)

        st.session_state["rewritten_text"] = rewritten

        # Generate timestamp once and store it
        timestamp = datetime.utcnow().isoformat() + "Z"
        st.session_state["last_rewrite_timestamp"] = timestamp

        # Save history
        history.add(
            original_text=st.session_state["input_text"],
            rewritten_text=rewritten,
            audience=audience,
            tone=tone,
            target_length=target_length,
            formality=formality_slider,
            created_at=timestamp,
        )

    rewritten_text = st.session_state.get("rewritten_text", "")

    # This dictionary holds all data for the current rewrite event
    current_rewrite_data = {
        "original_text": st.session_state.get("input_text", ""),
        "rewritten_text": rewritten_text,
        "audience": audience,
        "tone": tone,
        "timestamp": st.session_state.get("last_rewrite_timestamp", "")
    }

    if rewritten_text:
        st.markdown(
    "<h2 style='color:#FFFFFF;font-size:34px;font-weight:700;'>📝 Rewritten Text</h2>",
    unsafe_allow_html=True,
)
        st.text_area("", rewritten_text, height=240, key="output_text")

        analysis = analyze_text(rewritten_text)
        st.markdown(
    "<h2 style='color:#FFFFFF;font-size:34px;font-weight:700;'>📊 Text Analysis</h2>",
    unsafe_allow_html=True,
)
        st.metric("Word Count", analysis["word_count"])
        st.metric("Character Count", analysis["char_count"])
        st.metric("Readability", analysis["readability_label"])
        st.plotly_chart(analysis["charts"]["char_dist"], use_container_width=True)
        st.plotly_chart(analysis["charts"]["readability_bar"], use_container_width=True)

        st.markdown(
    "<h2 style='color:#FFFFFF;font-size:34px;font-weight:700;'>📦 Export</h2>",
    unsafe_allow_html=True,
)
        out_name = "tonesshift_rewrite"
        colA, colB, colC = st.columns(3)

        with colA:
            if st.download_button(
                "Download TXT",
                data=export_txt(current_rewrite_data),
                file_name=f"{out_name}.txt",
                mime="text/plain",
                use_container_width=True,
            ):
                pass

        with colB:
            if st.download_button(
                "Download DOCX",
                data=export_docx(current_rewrite_data),
                file_name=f"{out_name}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
            ):
                pass

        with colC:
            if st.download_button(
                "Download PDF",
                data=export_pdf(current_rewrite_data),
                file_name=f"{out_name}.pdf",
                mime="application/pdf",
                use_container_width=True,
            ):
                pass

        st.markdown(
    "<h2 style='color:#FFFFFF;font-size:34px;font-weight:700;'>🔊 Voice</h2>",
    unsafe_allow_html=True,
)
        if st.button("Play with Voice", use_container_width=True):
            audio_bytes, mime = text_to_speech(rewritten_text)
            st.audio(audio_bytes, format=mime)

    st.divider()
    hist_col1, hist_col2 = st.columns([3, 1])
    hist_col1.markdown(
    "<h2 style='color:#FFFFFF;font-size:34px;font-weight:700;'>📜 History</h2>",
    unsafe_allow_html=True,
)

    hist = history.list()

    if hist:
        if hist_col2.button("Clear All History", use_container_width=True, type="secondary"):
            history.clear()
            st.experimental_rerun()

    if not hist:
        st.info("No history yet.")
    else:
        recent_history = list(reversed(hist))[:5]

        for i, item in enumerate(recent_history):
            ts = datetime.fromisoformat(
                item["created_at"].replace("Z", "+00:00")
            ).strftime("%Y-%m-%d %H:%M")

            with st.expander(f"**{item['audience']} / {item['tone']}** at {ts}"):

                st.markdown("### ✨ Rewritten")
    st.code(item["rewritten_text"], language=None)

    st.markdown("### 📄 Original")
    st.code(item["original_text"], language=None)


    btn_cols = st.columns(2)

    if btn_cols[0].button(
                    "Restore",
                    key=f"restore_{i}",
                    use_container_width=True,
                ):
                    st.session_state["input_text"] = item["original_text"]
                    st.session_state["rewritten_text"] = item["rewritten_text"]
                    st.success("Restored text to input/output areas.")
                    st.experimental_rerun()

    if btn_cols[1].button(
                    "Delete",
                    key=f"delete_{i}",
                    use_container_width=True,
                ):
                    history.delete(item["created_at"])
                    st.experimental_rerun()


if __name__ == "__main__":
    main()