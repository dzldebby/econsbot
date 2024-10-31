import streamlit as st
import graphviz

st.set_page_config(
    page_title="Methodology - Textbook Assistant",
    page_icon="🔍",
    layout="wide"
)

st.title("Methodology")
st.write("Learn about the technical implementation and approaches used in our application.")

# Feature 1: Ask My Textbook
st.header("1. Ask My Textbook - Question Answering System")
st.write("""
Our textbook Q&A system uses Retrieval-Augmented Generation (RAG) to provide accurate, 
context-aware responses to your questions.
""")

# Create RAG flow diagram
rag_flow = graphviz.Digraph()
rag_flow.attr(rankdir='LR')
rag_flow.attr('node', shape='box')

# Add nodes
rag_flow.node('A', 'PDF Textbook')
rag_flow.node('B', 'Text Chunks')
rag_flow.node('C', 'Vector\nEmbeddings')
rag_flow.node('D', 'Vector Store\n(FAISS)')
rag_flow.node('E', 'User Question')
rag_flow.node('F', 'Retrieved\nContext')
rag_flow.node('G', 'LLM Response')

# Add edges
rag_flow.edge('A', 'B', 'Split')
rag_flow.edge('B', 'C', 'Embed')
rag_flow.edge('C', 'D', 'Store')
rag_flow.edge('E', 'D', 'Query')
rag_flow.edge('D', 'F', 'Retrieve')
rag_flow.edge('F', 'G', 'Generate')
rag_flow.edge('E', 'G', 'Context')

st.graphviz_chart(rag_flow)

st.subheader("Technical Components")
st.markdown("""
- **Document Processing**:
  - PyPDFLoader for PDF parsing
  - RecursiveCharacterTextSplitter for text chunking
  - Chunk size: 1000 characters with 200 character overlap

- **Vector Embeddings**:
  - OpenAI's text-embedding-3-small model
  - FAISS vector store for efficient similarity search
  - Top-4 most relevant chunks retrieved per query

- **Language Model**:
  - GPT-4 for response generation
  - Temperature set to 0.1 for consistent outputs
  - Custom prompt template for academic responses
""")

# Feature 2: Check My Answer
st.header("2. Check My Answer - Answer Evaluation System")
st.write("""
Our answer evaluation system uses structured prompting and assessment criteria to provide 
detailed feedback on economics answers.
""")

# Create evaluation flow diagram
eval_flow = graphviz.Digraph()
eval_flow.attr(rankdir='TB')
eval_flow.attr('node', shape='box')

# Add nodes
eval_flow.node('A', 'Student Answer')
eval_flow.node('B', 'Assessment\nObjectives')
eval_flow.node('C', 'LLM Analysis')
eval_flow.node('D', 'Structured\nFeedback')
eval_flow.node('E', 'AO Scores')
eval_flow.node('F', 'Improvement\nSuggestions')

# Add edges
eval_flow.edge('A', 'C')
eval_flow.edge('B', 'C')
eval_flow.edge('C', 'D')
eval_flow.edge('C', 'E')
eval_flow.edge('C', 'F')

st.graphviz_chart(eval_flow)

st.subheader("Assessment Framework")
st.markdown("""
- **Assessment Objectives**:
  - AO1: Knowledge and Understanding
  - AO2: Interpretation and Evaluation
  - AO3: Application and Analysis
  - AO4: Evaluation

- **Evaluation Components**:
  - Structured feedback on strengths
  - Areas for improvement
  - Numerical scoring (0-5) for each AO
  - Specific improvement suggestions

- **Technical Implementation**:
  - Custom prompt engineering
  - Consistent evaluation criteria
  - Constructive feedback generation
""")

st.header("Security Measures")
st.markdown("""
- Input validation and sanitization
- Prompt injection prevention
- Rate limiting and token controls
- Content safety checks
""")

# Footer
st.markdown("""
---
Questions about our methodology? Contact the development team through the [About Us](/About_Us) page.
""")
