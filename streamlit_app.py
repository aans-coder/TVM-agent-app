import streamlit as st
from orchestrator import handle_message

st.title("📊 TVM Solver Agent")
st.write("Ask me any Time Value of Money question — PV, FV, interest rate, or n.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("e.g. Find the FV of 10000 invested at 6% for 5 years"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = handle_message(prompt)
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
