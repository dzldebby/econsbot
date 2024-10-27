import streamlit as st

st.write("Testing secrets access:")
st.write(f"API Key exists: {'API_KEY' in st.secrets}")
st.write(f"API Base exists: {'API_BASE' in st.secrets}")