import streamlit as st
from qna_bot import qa_bot

st.title("DTC Q&A System")

with st.form(key='rag_form'):
    user_question = st.text_input("Enter your question:")
    submit_button = st.form_submit_button(label='Ask')

if submit_button and user_question.strip():
    with st.spinner("Retrieving and generating answer..."):
        response = qa_bot(user_question)
        st.markdown("Answer")
        st.markdown(response)
