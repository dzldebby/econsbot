import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationalRetrievalChain
import re
import os

# API Configuration
API_KEY = st.secrets["API_KEY"]
API_BASE = st.secrets["API_BASE"]
HEADERS = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/81.0"}

# At the top of your file, add page config with LaTeX support
st.set_page_config(
    page_title="Ask My Textbook",
    page_icon="📚",
    layout="wide"
)

# Security: Input validation function
def sanitize_input(text):
    # Remove any potential malicious characters or patterns
    sanitized = re.sub(r'[<>{}|\[\]`]', '', text)
    # Limit input length
    return sanitized[:1000]

# Define system prompt template
SYSTEM_TEMPLATE = """You are a helpful AI assistant focused on answering questions about the textbook content.
Your responses should be:
1. Based solely on the provided context
2. Academic and professional in tone
3. Clear and concise
4. Factual without speculation

For mathematical formulas:
- Use simple notation for basic terms (PED, YED, XED)
- For equations, write them plainly like: PED = %ΔQd/%ΔP
- Avoid complex LaTeX notation
- Use simple mathematical symbols when needed

If you're unsure or the question is outside the textbook's scope, say "I can only answer questions related to the textbook content."

Context: {context}
Current conversation: {chat_history}
Human: {question}
Assistant:"""

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "retriever" not in st.session_state:
    try:
        # Load and process the PDF
        with st.spinner('Loading PDF...'):
            loader = PyPDFLoader("Reference.pdf")
            documents = loader.load()
        
        with st.spinner('Processing content...'):
            # Split documents into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
                length_function=len
            )
            splits = text_splitter.split_documents(documents)
            
            # Create embeddings and vector store
            embeddings = OpenAIEmbeddings(
                model="text-embedding-3-small-prd-gcc2-lb",
                openai_api_key=API_KEY,
                openai_api_base=API_BASE,
                default_headers=HEADERS
            )
            
            vectorstore = FAISS.from_documents(splits, embeddings)
            st.session_state.retriever = vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 4}
            )
    except FileNotFoundError:
        st.error("Error: Textbook.pdf not found. Please make sure the file exists in the correct location.")
        st.stop()
    except Exception as e:
        st.error(f"An error occurred while loading the textbook: {str(e)}")
        st.stop()

# Initialize the chat model with specific parameters
with st.spinner('Initializing AI model...'):
    try:
        llm = ChatOpenAI(
            model="gpt-4o-prd-gcc2-lb",
            temperature=0.1,
            openai_api_key=API_KEY,
            openai_api_base=API_BASE,
            default_headers=HEADERS
        )

        # Create custom prompt
        PROMPT = PromptTemplate(
            input_variables=["context", "chat_history", "question"],
            template=SYSTEM_TEMPLATE
        )

        # Initialize the QA chain without memory
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=st.session_state.retriever,
            combine_docs_chain_kwargs={"prompt": PROMPT},
            return_source_documents=True,
            chain_type="stuff"
        )
    except Exception as e:
        st.error(f"An error occurred while initializing the AI model: {str(e)}")
        st.stop()

# Update the format_latex function
def format_latex(text):
    """Format text with basic replacements"""
    # Replace common economics formulas with plain text
    text = text.replace('\\text{PED}', 'PED')
    text = text.replace('\\text{YED}', 'YED')
    text = text.replace('\\text{XED}', 'XED')
    text = text.replace('\\frac', '')
    text = text.replace('\\Delta', 'Δ')
    text = text.replace('\\%', '%')
    
    # Remove any remaining LaTeX-style formatting
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'\$.*?\$', '', text)
    
    return text


# Main chat interface
st.title("Textbook Assistant")
st.write("""
Welcome to the Textbook Assistant! Ask any question about the textbook content, 
and I'll help you find the relevant information.
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

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input with security measures
if prompt := st.chat_input("Ask me about the textbook"):
    # Sanitize input
    clean_prompt = sanitize_input(prompt)
    
    # Check for potential prompt injection patterns
    if any(pattern in clean_prompt.lower() for pattern in [
        "ignore previous",
        "disregard",
        "forget",
        "system prompt",
        "you are now",
        "act as"
    ]):
        st.error("Invalid input detected. Please ask a legitimate question about the textbook.")
    else:
        # Display user message
        st.chat_message("user").markdown(clean_prompt)
        st.session_state.messages.append({"role": "user", "content": clean_prompt})
        
        try:
            with st.spinner('Thinking...'):
                # Get chatbot response without chat history
                result = qa_chain({
                    "question": clean_prompt,
                    "chat_history": []  # Empty chat history since we're not using memory
                })
                
                response = result["answer"]
                
                # Display assistant response
                # Display assistant response
                with st.chat_message("assistant"):
                    formatted_response = format_latex(response)
                    st.markdown(formatted_response)  # Changed from st.write to st.markdown
                st.session_state.messages.append({"role": "assistant", "content": formatted_response})



                # Optional: Display source documents for transparency
                if "source_documents" in result and result["source_documents"]:
                    with st.expander("View Sources"):
                        for doc in result["source_documents"]:
                            st.write(doc.page_content[:200] + "...")
        
        except Exception as e:
            st.error(f"An error occurred while processing your question: {str(e)}")

# Add a footer
st.markdown("""
---
Made with ❤️ by Christabelle and Debby | [About Us](/About_Us) | [Methodology](/Methodology)
""")
