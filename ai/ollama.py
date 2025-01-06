import streamlit as st
import sys
import ollama
from ifunctions import Message

mt = Message()
o = ollama.Client(host=st.secrets.ollama.host)
if 'ollama_history' not in st.session_state:
    st.session_state['ollama_history'] = []

def display_message(mt:dict,is_stream=False):
    '''展示用户与ollama的聊天框'''
    with st.chat_message(mt['role']):
        if is_stream:
            st.write_stream(mt['content'])
        else:
            st.write(mt['content'])

# 主界面
st.title('ollama test')

for message in st.session_state['ollama_history']:
    display_message(mt=message)

question = st.chat_input("question")
if question:
    display_message(mt = mt.user_mesasage(question))# 显示用户提问
    st.session_state['ollama_history'].append(mt.user_mesasage(question))# 保存用户提问
    response = o.chat(
        model=st.secrets.ollama.model,
        #messages=[mt.user_mesasage(question)],
        messages=st.session_state['ollama_history'],
        stream=False,
    )['message']['content']
    display_message(mt=mt.assistant_mesasage(response))# 显示ollama的回答
    st.session_state['ollama_history'].append(mt.assistant_mesasage(response))# 保存ollama的回答
