import streamlit as st
import google.generativeai as genai
import PyPDF2
import time
import easyocr
from pdf2image import convert_from_bytes


# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="🤖",
    layout="wide"
)

# =========================================
# GEMINI API
# =========================================

genai.configure(api_key="st.secrets["API_KEY"]

model = genai.GenerativeModel("gemini-2.5-flash")

# =========================================
# CUSTOM CSS
# =========================================

st.markdown("""
<style>

.stApp{
    background: linear-gradient(135deg,#0f172a,#020617);
}

.title{
    text-align:center;
    font-size:60px;
    font-weight:bold;
    color:white;
}

.subtitle{
    text-align:center;
    color:#cbd5e1;
    font-size:18px;
}

.stButton>button{
    width:100%;
    height:55px;
    border-radius:15px;
    border:none;
    background:linear-gradient(to right,#06b6d4,#3b82f6);
    color:white;
    font-size:18px;
    font-weight:bold;
}

.stButton>button:hover{
    transform:scale(1.02);
}

</style>
""", unsafe_allow_html=True)

# =========================================
# SIDEBAR
# =========================================

with st.sidebar:

    st.title("🤖 AI Study Buddy")

    st.markdown("---")

    st.markdown("### Features")

    st.markdown("""
    ✅ Summary

    ✅ Easy Explanation

    ✅ Important Questions

    ✅ MCQ Generator

    ✅ Viva Questions

    ✅ Marathi Explanation

    ✅ Notes Summarizer
    """)

    st.markdown("---")

    st.success("Developed by Yash 😎")

# =========================================
# HEADER
# =========================================

st.markdown(
    "<h1 class='title'>AI Study Buddy</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p class='subtitle'>Your Personal AI Exam Assistant 🚀</p>",
    unsafe_allow_html=True
)

# =========================================
# PDF UPLOAD
# =========================================

uploaded_file = st.file_uploader(
    "📄 Upload PDF Notes",
    type=["pdf"]
)

# =========================================
# PDF READER FUNCTION
# =========================================

def read_pdf(file):
    reader = easyocr.Reader(['en'])

    images = convert_from_bytes(
        file.read(),
        poppler_path=r"C:\Users\admin\Downloads\Release-26.02.0-0\poppler-26.02.0\Library\bin"
    )

    text = ""

    for img in images:
        result = reader.readtext(img)

        for item in result:
            text += item[1] + " "

    return text

# =========================================
# IF PDF UPLOADED
# =========================================

if uploaded_file:

    st.success("PDF Uploaded Successfully ✅")

    pdf_text = read_pdf(uploaded_file)

    st.subheader("PDF Extracted Text")

    st.write(pdf_text[:3000])
    st.write("Length =", len(pdf_text))

    st.info(f"📄 File Name: {uploaded_file.name}")
    # =========================================
    # FEATURE SELECT
    # =========================================

    option = st.selectbox(
        "🎯 Choose Feature",
        [
            "Summary",
            "Easy Explanation",
            "Important Questions",
            "MCQ Generator",
            "Viva Questions",
            "Marathi Explanation",
            "Notes Summarizer",
            "Chat With PDF",
            
        ]
    )

        # =========================================
    # CHAT WITH PDF
    # =========================================

    if option == "Chat With PDF":

        st.subheader("💬 Chat With PDF")

        user_question = st.text_input(
            "Ask anything from PDF"
        )

        if st.button("🤖 Ask AI"):

            chat_prompt = f"""
            Answer only using the PDF notes.

            PDF Notes:
            {pdf_text[:8000]}

            Question:
            {user_question}

            Give a short and clear answer.
            """

            with st.spinner("🤖 Thinking..."):

                response = model.generate_content(
                    chat_prompt
                )

            st.markdown("---")
            st.subheader("💬 Answer")
            st.write(response.text)

    # =========================================
    # GENERATE BUTTON
    # =========================================

    if st.button("🚀 Generate AI Output"):

        if option == "Summary":
            prompt = f"Give a short summary of these notes:\n\n{pdf_text[:12000]}"

        elif option == "Easy Explanation":
            prompt = f"Explain these notes in very simple language:\n\n{pdf_text[:12000]}"

        elif option == "Important Questions":
            prompt = f"Generate 15 important exam questions from:\n\n{pdf_text[:12000]}"

        elif option == "MCQ Generator":
            prompt = f"Generate 20 MCQs with answers from:\n\n{pdf_text[:12000]}"

        elif option == "Viva Questions":
            prompt = f"Generate 20 viva questions with answers from:\n\n{pdf_text[:12000]}"

        elif option == "Marathi Explanation":
            prompt = f"Explain these notes in Marathi:\n\n{pdf_text[:12000]}"

        elif option == "Notes Summarizer":
            prompt = f"Create short revision notes from:\n\n{pdf_text[:12000]}"

        with st.spinner("🤖 AI Thinking..."):
            response = model.generate_content(prompt)

        st.markdown("---")
        st.subheader("🤖 AI Output")
        st.write(response.text)
