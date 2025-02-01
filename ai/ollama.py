import streamlit as st
import sys,time
import ollama
from ifunctions import Message
from pydantic import BaseModel
ollama_system_tip = st.empty()
mt = Message()
o = ollama.Client(host=st.secrets.ollama.host)
if 'ollama_history' not in st.session_state:
    st.session_state['ollama_history'] = []
def get_ollama_list():
    model_list = o.list()
    return model_list
def clear_GPU():
    o.chat(model=model_name,messages=[],stream=False,keep_alive=0)
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
model_name_list = [x.model for x in get_ollama_list()['models']]

with st.sidebar:
    model_name = st.selectbox('选择模型',model_name_list)
    is_stream = st.checkbox('流式响应',value=True)
    #st.write(is_stream)
    if st.button('清除历史记录',type='primary'):
        st.session_state['ollama_history'] = []
    if st.button('释放显存',type='primary'):
        clear_GPU()
# 主界面
st.title(f'{model_name.split(":")[0]}')
st.caption('与 ollama 加载的模型进行聊天')
question = st.chat_input("question")
with st.container():
    ollama_system_tip.info('请在下方输入你的问题开始生成：')
    # 显示历史记录
    for message in st.session_state['ollama_history']:
        ollama_system_tip.empty()
        display_message(mt=message)
    if question:
        ollama_system_tip.empty()
        display_message(mt = mt.user_mesasage(question))# 显示用户提问
        st.session_state['ollama_history'].append(mt.user_mesasage(question))# 保存用户提问
        temp_response = o.chat(model=model_name,messages=st.session_state['ollama_history'],stream=is_stream,)# 获取ollama的回答
        if is_stream:
            meta_stream_text = stream_chunk(temp_response)# 流式输出
            response = display_message(mt=mt.assistant_mesasage(meta_stream_text),is_stream=is_stream)# 显示ollama的回答
        else:
            response = temp_response['message']['content']
            display_message(mt=mt.assistant_mesasage(response))# 显示ollama的回答
        st.session_state['ollama_history'].append(mt.assistant_mesasage(response))# 保存ollama的回答
