import streamlit as st
import sys,time
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
            return st.write_stream(mt['content'])
        else:
            st.write(mt['content'])
def stream_chunk(chunks):
    for chunk in chunks:
        time.sleep(st.secrets.ollama.stream_delay)
        yield chunk['message']['content']
# 侧边栏
with st.sidebar:
    is_stream = st.checkbox('流式响应',value=False)
    st.write(is_stream)
# 主界面
st.title('ollama test')
# 显示历史记录
for message in st.session_state['ollama_history']:
    display_message(mt=message)

question = st.chat_input("question")
if question:
    display_message(mt = mt.user_mesasage(question))# 显示用户提问
    st.session_state['ollama_history'].append(mt.user_mesasage(question))# 保存用户提问
    temp_response = o.chat(model=st.secrets.ollama.model,messages=st.session_state['ollama_history'],stream=is_stream,)#['message']['content']# 获取ollama的回答
    if is_stream:
        meta_stream_text = stream_chunk(temp_response)# 流式输出
        response = display_message(mt=mt.assistant_mesasage(meta_stream_text),is_stream=is_stream)# 显示ollama的回答
        

    else:
        response = temp_response['message']['content']
        display_message(mt=mt.assistant_mesasage(response))# 显示ollama的回答
    st.session_state['ollama_history'].append(mt.assistant_mesasage(response))# 保存ollama的回答
