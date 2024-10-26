import streamlit as st

st.set_page_config(
    page_title="About Us - Textbook Assistant",
    page_icon="ℹ️",
    layout="wide"
)

st.title("About Us")

st.header("Project Overview")
st.write("""
Our Textbook Assistant is an innovative AI-powered application designed to revolutionize 
how students interact with their educational materials. By leveraging advanced language 
models and retrieval-augmented generation (RAG), we provide intelligent, context-aware 
responses to questions about textbook content.
""")

# Project Details in Columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("Objectives")
    st.write("""
    - Provide instant, accurate answers to textbook-related queries
    - Enhance learning experience through interactive Q&A
    - Ensure reliable and source-backed information
    - Make textbook content more accessible and engaging
    - Support self-paced learning
    """)
    
    st.subheader("Data Sources")
    st.write("""
    - Primary Textbook (PDF format)
    - Processed using advanced text splitting techniques
    - Embedded using OpenAI's text-embedding-3-small model
    - Stored in FAISS vector database for efficient retrieval
    """)

with col2:
    st.subheader("Key Features")
    st.write("""
    - Real-time question answering
    - Context-aware responses
    - Source citation and transparency
    - Conversation memory
    - Security measures against prompt injection
    - Professional and academic response tone
    """)
    
    st.subheader("Technology Stack")
    st.write("""
    - LangChain for LLM orchestration
    - OpenAI's GPT-4 for text generation
    - FAISS for vector similarity search
    - Streamlit for user interface
    - Python for backend processing
    """)

st.header("Our Commitment")
st.write("""
We are committed to providing accurate, reliable, and educational responses while maintaining 
the highest standards of academic integrity. Our system is designed to complement traditional 
learning methods, not replace them.
""")
