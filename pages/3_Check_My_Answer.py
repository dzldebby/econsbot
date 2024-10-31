import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

st.set_page_config(
    page_title="Check My Answer - Textbook Assistant",
    page_icon="✅",
    layout="wide"
)

# API Configuration
API_KEY = st.secrets["API_KEY"]
API_BASE = st.secrets["API_BASE"]
HEADERS = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/81.0"}

# Assessment criteria template
ASSESSMENT_TEMPLATE = """You are an experienced economics teacher evaluating a student's answer. 
Assess the answer based on these Assessment Objectives (AOs):

AO1: Knowledge and Understanding
- Demonstrate knowledge and understanding of economic concepts, theories and principles.

AO2: Interpretation and Evaluation of Information
- Interpret economic information presented in textual, numerical or graphical form.
- Make valid inferences based on the information presented and its limitations.

AO3: Application and Analysis
- Apply relevant economic concepts, theories and principles to analyse contemporary issues, perspectives and policy choices.
- Construct coherent economic arguments.

AO4: Evaluation
- Evaluate critically contemporary issues, perspectives and policy choices.
- Recognise unstated assumptions and evaluate their relevance.
- Synthesise economic arguments to arrive at well-reasoned judgements and decisions.

Question: {question}
Student's Answer: {answer}

Provide a detailed evaluation following this structure:
1. Strengths (what the answer did well)
2. Areas for Improvement (what could be better)
3. Score for each AO (out of 5)
4. Overall Assessment
5. Specific Suggestions for Improvement

Remember to be constructive and encouraging while maintaining high academic standards.

Response:"""

def initialize_llm():
    """Initialize the language model"""
    try:
        return ChatOpenAI(
            model="gpt-4o-prd-gcc2-lb",
            temperature=0.1,
            openai_api_key=API_KEY,
            openai_api_base=API_BASE,
            default_headers=HEADERS
        )
    except Exception as e:
        st.error(f"Error initializing AI model: {str(e)}")
        return None

def evaluate_answer(question, answer, llm):
    """Evaluate the student's answer using the LLM"""
    try:
        prompt = PromptTemplate(
            input_variables=["question", "answer"],
            template=ASSESSMENT_TEMPLATE
        )
        
        # Get evaluation from LLM
        messages = [{"role": "user", "content": prompt.format(question=question, answer=answer)}]
        response = llm.invoke(messages)
        
        return response.content
    except Exception as e:
        st.error(f"Error evaluating answer: {str(e)}")
        return None

# Main UI
st.title("Check My Answer")
st.write("""
Get detailed feedback on your economics answer based on official assessment objectives.
Enter your question and answer below for a comprehensive evaluation.
""")

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


# Initialize session state for storing previous evaluations
if 'evaluations' not in st.session_state:
    st.session_state.evaluations = []

# Input fields
question = st.text_area("Enter the economics question:", height=100)
answer = st.text_area("Enter your answer:", height=200)

# Initialize LLM
llm = initialize_llm()

if st.button("Evaluate My Answer"):
    if not question or not answer:
        st.warning("Please provide both a question and an answer.")
    else:
        with st.spinner("Evaluating your answer..."):
            evaluation = evaluate_answer(question, answer, llm)
            if evaluation:
                # Store evaluation in session state
                st.session_state.evaluations.append({
                    "question": question,
                    "answer": answer,
                    "evaluation": evaluation
                })
                
                # Display evaluation
                st.success("Evaluation complete!")
                st.markdown("### Feedback")
                st.markdown(evaluation)

# Show previous evaluations
if st.session_state.evaluations:
    st.markdown("### Previous Evaluations")
    for i, eval_item in enumerate(st.session_state.evaluations):
        with st.expander(f"Evaluation {i+1}: {eval_item['question'][:50]}..."):
            st.markdown("**Question:**")
            st.write(eval_item['question'])
            st.markdown("**Your Answer:**")
            st.write(eval_item['answer'])
            st.markdown("**Feedback:**")
            st.markdown(eval_item['evaluation'])

# Add helpful tips
st.sidebar.header("Tips for Better Answers (Based on GCE 'A' Levels Syllabus)")
st.sidebar.markdown("""
### Assessment Objectives (AOs)

**AO1: Knowledge and Understanding**
- Use economic terminology correctly
- Define key concepts
- Show understanding of theories

**AO2: Interpretation**
- Use data effectively
- Draw valid conclusions
- Acknowledge limitations

**AO3: Application**
- Link theory to real examples
- Build logical arguments
- Show cause-effect relationships

**AO4: Evaluation**
- Consider different perspectives
- Identify assumptions
- Make reasoned judgements
""")

# Footer
st.markdown("""
---
Need help improving your answers? Check out the [Methodology](/Methodology) page for tips on structuring economic arguments.
""") 