import streamlit as st
import ifunctions as ifs

# 初始化参数
mg = ifs.Message()
if 'qwen_history' not in st.session_state:
    st.session_state['qwen_history'] = []

st.title('通义千问')
st.caption('调用阿里云百炼 api ，悠着点用。')

temp_question = st.chat_input("question")



