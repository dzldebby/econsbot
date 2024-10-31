import streamlit as st

st.set_page_config(
    page_title="Economics AI Assistant",
    page_icon="🎓",
    layout="wide"
)

# Then add password protection
def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == "12345":
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password
        st.text_input(
            "Please enter the password", 
            type="password", 
            on_change=password_entered, 
            key="password"
        )
        return False
    
    elif not st.session_state["password_correct"]:
        # Password incorrect, show input + error
        st.text_input(
            "Please enter the password", 
            type="password", 
            on_change=password_entered, 
            key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct
        return True

# Check password
if not check_password():
    st.stop()  # Do not continue if check_password is False

# Main content
st.title("Welcome to Economics AI Assistant")

# Add disclaimer in an expander
with st.expander("⚠️ IMPORTANT DISCLAIMER - Please Read"):
    st.warning("""
    IMPORTANT NOTICE: This web application is developed as a proof-of-concept prototype. 
    The information provided here is NOT intended for actual usage and should not be relied 
    upon for making any decisions, especially those related to financial, legal, or healthcare matters.

    Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. 
    You assume full responsibility for how you use any generated output.

    Always consult with qualified professionals for accurate and personalized advice.
    """)

st.markdown("""
Welcome to your AI-powered economics learning companion! This application offers two main features 
to enhance your economics study experience:
""")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 📚 [Ask My Textbook](/Ask_My_Textbook)
    
    An intelligent Q&A system that helps you:
    - Ask questions about the textbook content
    - Get accurate, context-aware answers
    - Access specific information quickly
    - Understand complex economics concepts
    
    [Try Ask My Textbook →](/Ask_My_Textbook)
    """)

with col2:
    st.markdown("""
    ### ✅ [Check My Answer](/Check_My_Answer)
    
    An automated answer evaluation system that:
    - Assesses your economics answers
    - Provides detailed feedback
    - Scores based on assessment objectives
    - Offers improvement suggestions
    
    [Try Check My Answer →](/Check_My_Answer)
    """)

st.markdown("---")

# About the Textbook
st.header("About the Textbook")
st.markdown("""
This AI assistant is powered by **"GCE A Level Economics: The Examination Skills Guide"**, authored by 
**Christabelle Soh**. The integration of author expertise with AI technology ensures high-quality, 
examination-focused support for your economics studies.
""")

# Getting Started
st.header("Getting Started")
st.markdown("""
1. **For Content Questions**:
   - Navigate to [Ask My Textbook](/Ask_My_Textbook)
   - Type your economics question
   - Receive detailed, contextual answers

2. **For Answer Evaluation**:
   - Go to [Check My Answer](/Check_My_Answer)
   - Enter the question and your answer
   - Get comprehensive feedback and scores

3. **To Learn More**:
   - Visit [Methodology](/Methodology) for technical details
   - Check [About Us](/About_Us) to meet the team
""")

# Footer
st.markdown("""
---
Made with ❤️ by Christabelle and Debby | [About Us](/About_Us) | [Methodology](/Methodology)
""")
