import streamlit as st

st.set_page_config(
    page_title="About Us - Textbook Assistant",
    page_icon="👥",
    layout="wide"
)

st.title("About Us")

# Project Overview
st.header("Project Overview")
st.write("""
We've developed an AI-powered educational assistant that combines two key features:
1. **Ask My Textbook**: An intelligent Q&A system for textbook content
2. **Check My Answer**: An automated answer evaluation system based on assessment objectives
""")

# Team Members
st.header("Meet the Team")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Christabelle")
    st.write("""
    Role: Domain Lead
    - Expertise in educational technology
    - Background in economics education
    - Focus on user experience and educational value
    """)

with col2:
    st.subheader("Debby")
    st.write("""
    Role: Technical Lead
    - Expertise in AI/ML implementation
    - Background in software development
    - Focus on system architecture and security
    """)

# Project Goals
st.header("Project Goals")
st.markdown("""
1. **Enhanced Learning Support**
   - Provide instant access to textbook information
   - Offer structured feedback on student answers
   - Support self-paced learning

2. **Educational Innovation**
   - Implement RAG technology for accurate responses
   - Develop systematic answer evaluation
   - Maintain academic standards

3. **Accessibility**
   - Create user-friendly interface
   - Provide clear, constructive feedback
   - Support different learning styles
""")

# Technology Stack
st.header("Technology Stack")
st.markdown("""
- **Frontend**: Streamlit
- **AI/ML**: 
  - OpenAI GPT-4
  - LangChain
  - FAISS Vector Store
- **Document Processing**:
  - PyPDF
  - Text Embeddings
- **Security**:
  - Input validation
  - Rate limiting
  - Content filtering
""")

# Contact Information
st.header("Contact Us")
st.write("""
For questions, suggestions, or feedback, please reach out to us:
- Email: [contact@example.com](mailto:contact@example.com)
- GitHub: [Project Repository](https://github.com/dzldebby/econsbot)
""")

# Footer
st.markdown("""
---
Thank you for using our application! Check out our [Methodology](/Methodology) page to learn more about how it works.
""")
