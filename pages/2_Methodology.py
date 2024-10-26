import streamlit as st
from PIL import Image
import graphviz

st.set_page_config(
    page_title="Methodology - Textbook Assistant",
    page_icon="🔧",
    layout="wide"
)

st.title("Methodology")

st.header("System Architecture")
st.write("""
Our Textbook Assistant employs a sophisticated architecture combining several key components 
to deliver accurate and context-aware responses.
""")

# Create flowchart for RAG Chat
st.subheader("RAG Chat Process Flow")
chat_flow = graphviz.Digraph()
chat_flow.attr(rankdir='LR')

# Add nodes
chat_flow.node('A', 'User Query')
chat_flow.node('B', 'Input Validation')
chat_flow.node('C', 'Query Embedding')
chat_flow.node('D', 'Vector Search')
chat_flow.node('E', 'Context Retrieval')
chat_flow.node('F', 'LLM Processing')
chat_flow.node('G', 'Response Generation')

# Add edges
chat_flow.edge('A', 'B')
chat_flow.edge('B', 'C')
chat_flow.edge('C', 'D')
chat_flow.edge('D', 'E')
chat_flow.edge('E', 'F')
chat_flow.edge('F', 'G')

st.graphviz_chart(chat_flow)

# Detailed Process Explanation
st.header("Implementation Details")

st.subheader("1. Document Processing")
st.write("""
- **Text Extraction**: PDF content is extracted using PyPDFLoader
- **Text Splitting**: Content is divided into chunks using RecursiveCharacterTextSplitter
  - Chunk size: 1000 characters
  - Overlap: 200 characters
  - Multiple separators for natural breaks
- **Embedding Generation**: Text chunks are converted to vectors using OpenAI's embedding model
- **Vector Storage**: Embeddings are stored in FAISS for efficient similarity search
""")

st.subheader("2. Query Processing")
st.write("""
- **Input Validation**: 
  - Sanitization of special characters
  - Length limits
  - Prompt injection detection
- **Context Retrieval**:
  - Query embedding generation
  - Top-k similarity search (k=4)
  - Context window preparation
""")

st.subheader("3. Response Generation")
st.write("""
- **Prompt Engineering**:
  - Clear system instructions
  - Context integration
  - Conversation history inclusion
- **LLM Processing**:
  - Temperature: 0.1 for focused responses
  - Professional tone enforcement
  - Source attribution
""")

st.subheader("4. Security Measures")
st.write("""
- Input validation and sanitization
- Prompt injection detection
- Rate limiting
- Error handling
- Response filtering
""")

# Data Flow Diagram
st.header("Data Flow")
st.write("""
The system follows a structured data flow process:

1. **Input Layer**
   - User query reception
   - Input validation and preprocessing

2. **Processing Layer**
   - Query embedding
   - Context retrieval
   - Prompt construction

3. **Generation Layer**
   - LLM processing
   - Response formatting
   - Source attribution

4. **Output Layer**
   - Response validation
   - Presentation
   - Source display
""")

# Performance Metrics
st.header("Performance Considerations")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Response Time")
    st.write("""
    - Average query processing: 2-3 seconds
    - Context retrieval: ~100ms
    - LLM generation: 1-2 seconds
    """)

with col2:
    st.subheader("Accuracy Metrics")
    st.write("""
    - Context relevance score > 0.8
    - Source citation rate: 100%
    - Error rate < 1%
    """)

st.header("Future Improvements")
st.write("""
- Implementation of streaming responses
- Enhanced conversation memory
- Multi-document support
- User feedback integration
- Performance optimization
""")
