import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings  # Updated import
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI  # Updated import
from langchain.prompts import PromptTemplate
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationalRetrievalChain  # Added missing import
import re


st.set_page_config(page_title="Textbook Assistant", page_icon="📚", layout="wide")


# API Configuration
API_KEY = "sk-9yferRaarrs_xmdJKA3uMg"
API_BASE = "https://litellm.govtext.gov.sg/"
HEADERS = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/81.0"}

# Security: Input validation function
def sanitize_input(text):
    # Remove any potential malicious characters or patterns
    sanitized = re.sub(r'[<>{}|\[\]`]', '', text)
    # Limit input length
    return sanitized[:1000]

# Define system prompt template with clear boundaries and instructions
SYSTEM_TEMPLATE = """You are a helpful AI assistant focused on answering questions about the textbook content.
Your responses should be:
1. Based solely on the provided context
2. Academic and professional in tone
3. Clear and concise
4. Factual without speculation

If you're unsure or the question is outside the textbook's scope, say "I can only answer questions related to the textbook content."

Context: {context}
Current conversation: {chat_history}
Human: {question}
Assistant:"""

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "retriever" not in st.session_state:
    # Load and process the PDF
    loader = PyPDFLoader("Reference.pdf")
    documents = loader.load()
    
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
        search_kwargs={"k": 4}  # Fetch top 4 most relevant chunks
    )

# Initialize the chat model with specific parameters
llm = ChatOpenAI(
    model="gpt-4o-prd-gcc2-lb",
    temperature=0.1,  # Lower temperature for more focused responses
    openai_api_key=API_KEY,
    openai_api_base=API_BASE,
    default_headers=HEADERS
)

# Create conversation memory
memory = ConversationBufferWindowMemory(
    memory_key="chat_history",
    k=3,  # Remember last 3 exchanges
    return_messages=True
)

# Create custom prompt
PROMPT = PromptTemplate(
    input_variables=["context", "chat_history", "question"],
    template=SYSTEM_TEMPLATE
)

# Initialize the QA chain with memory and custom prompt
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=st.session_state.retriever,
    memory=memory,
    combine_docs_chain_kwargs={"prompt": PROMPT},
    return_source_documents=True,
    verbose=True
)

st.title("Textbook Assistant")

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
            # Get chatbot response
            result = qa_chain({
                "question": clean_prompt,
                "chat_history": [(msg["role"], msg["content"]) 
                               for msg in st.session_state.messages[-6:]]  # Last 3 exchanges
            })
            response = result["answer"]
            
            # Display assistant response
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Optional: Display source documents for transparency
            if "source_documents" in result and result["source_documents"]:
                with st.expander("View Sources"):
                    for doc in result["source_documents"]:
                        st.write(doc.page_content[:200] + "...")
        
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
