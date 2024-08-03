import streamlit as st
from backend import redact_pdf, save_to_csv, load_language_model
import io

# Streamlit App
st.set_page_config(
    page_title="PDF Processing App",
    page_icon=":bookmark_tabs:",
    layout="wide"
)

# Sidebar
st.sidebar.header("PDF Processing App")
logo_path = "/frontend/assests/logo.png"  # Update this to your correct relative path
try:
    st.sidebar.image(logo_path, use_column_width=True)
except FileNotFoundError:
    st.sidebar.error("Logo image not found at path: " + logo_path)

st.sidebar.markdown("## Upload and Process your PDF")
st.sidebar.markdown(
    """
    Welcome to the PDF Processing App!
    
    Upload a PDF file, and we will process it for you. After processing, you'll be able to download the result.
    """
)

# Language selection
language = st.sidebar.selectbox(
    "Select the language of your PDF",
    ["English", "German", "Mandarin", "Malaysian", "Korean"]
)

# Load the language-specific model
tagger = load_language_model(language)

# Main content
st.title("PDF Processing App")
st.markdown(
    """
    Upload your PDF file below. We will process it and provide a download link for the processed PDF.
    """
)

uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

if uploaded_file:
    st.write("Processing the PDF...")
    
    with st.spinner('Processing...'):
        # Ensure the uploaded file is passed as a BytesIO stream
        processed_pdf, page_data = redact_pdf(uploaded_file, tagger, language)
        csv_data = save_to_csv(page_data)
    
    st.success("Processing complete!")
    st.download_button(
        label="Download Processed PDF",
        data=processed_pdf.getvalue(),
        file_name="processed.pdf",
        mime="application/pdf"
    )
    st.download_button(
        label="Download CSV",
        data=csv_data,
        file_name="data.csv",
        mime="text/csv"
    )

st.markdown(
    """
    <style>
    .reportview-container {
        background: #f0f2f6;
    }
    .sidebar .sidebar-content {
        background: #ffffff;
    }
    .stButton>button {
        background-color: #007bff;
        color: white;
        border: none;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
    </style>
    """,
    unsafe_allow_html=True
)
