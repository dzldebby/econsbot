import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
import os

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = "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"

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
        chunk_overlap=200
    )
    splits = text_splitter.split_documents(documents)
    
    # Create embeddings and vector store
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(splits, embeddings)
    st.session_state.retriever = vectorstore.as_retriever()

# Initialize the chat model and chain
llm = ChatOpenAI(temperature=0)
qa_chain = ConversationalRetrievalChain.from_llm(
    llm,
    st.session_state.retriever,
    return_source_documents=True
)

st.title("Textbook Assistant")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Ask me about the textbook"):
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Get chatbot response
    result = qa_chain({"question": prompt, "chat_history": []})
    response = result["answer"]
    
    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
