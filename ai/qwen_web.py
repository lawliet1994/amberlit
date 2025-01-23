import streamlit as st
import sys,os
import ifunctions as ifs
import json
import random
from http import HTTPStatus
from dashscope import Generation
from openai import OpenAI
# 初始化参数
mg = ifs.Message()
model_dict = {
    'qwen-turbo':'适合简单任务，速度快、成本低',
    'qwq-32b-preview':'QwQ 模型是由 Qwen 团队开发的实验性研究模型，专注于增强 AI 推理能力，尤其是数学和编程领域。',
    'qvq-72b-preview':'QVQ模型是由 Qwen 团队开发的实验性研究模型，专注于提升视觉推理能力，尤其在数学推理领域。',
    'qwen-coder-plus':'Qwen 的代码模型',
    'qwen-max':'适合复杂任务，推理能力最强',
    'qwen-plus':'效果、速度、成本均衡',
    'qwen-long':'持长达千万字文档，成本低',
}
model_list = model_dict.keys()
if 'qwen_history' not in st.session_state:
    st.session_state['qwen_history'] = []
def get_response(model,messages):
    responses = Generation.call(model=model,
                                messages=messages,
                                # 设置随机数种子seed，如果没有设置，则随机数种子默认为1234
                                seed=random.randint(1, 10000),
                                # 将输出设置为"message"格式
                                result_format='message',
                                stream=True,
                                incremental_output=True,
                                api_key=st.secrets.qwen.API_KEY)
    for response in responses:
        if response.status_code == HTTPStatus.OK:
            yield response.output.choices[0]['message']['content']
def get_response_without_streaming(model,messages):
    # responses = Generation.call(model=model,
    #                             messages=messages,
    #                             # 设置随机数种子seed，如果没有设置，则随机数种子默认为1234
    #                             seed=random.randint(1, 10000),
    #                             # 将输出设置为"message"格式
    #                             result_format='message',
    #                             stream=False,
    #                             incremental_output=True,
    #                             api_key=st.secrets.qwen.API_KEY) 
    client = OpenAI(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
        api_key=st.secrets.qwen.API_KEY, 
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    completion = client.chat.completions.create(
        model=model, # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages=messages
        )
        
    print(completion.model_dump_json())
    return completion.model_dump_json()
#############################################***************主界面***************#############################################
# 侧边栏
with st.sidebar:
    st.title('参数设置')
    model_selected = st.selectbox('选择模型',model_list)
    # with st.popover('模型简介',use_container_width=1):
    #     st.write(model_dict[model_selected])
    is_streaming = st.checkbox('流式输出',value=True)
    if st.button('清除历史记录',type='primary'):
        st.session_state['qwen_history'] = []

# 主界面
st.title('通义千问')
st.caption(f'{model_selected}，{model_dict[model_selected]}。')

temp_question = st.chat_input("question")

# 展示历史记录
for message in st.session_state['qwen_history']:
    with st.chat_message(message['role']):
        st.write(message['content'])

if temp_question:
    with st.chat_message("user"):
        st.write(temp_question)
    question = mg.user_mesasage(temp_question)
    st.session_state['qwen_history'].append(question)
    # for response in get_response(st.session_state['qwen_history']):
    #     full_response = st.write(response)
    with st.chat_message("assistant"):
        if is_streaming:
            full_response = st.write_stream(get_response(model=model_selected,messages=st.session_state['qwen_history']))
        else:
            full_response = json.loads(get_response_without_streaming(model=model_selected,messages=st.session_state['qwen_history']))['choices'][0]['message']['content']
            st.write(full_response)
    st.session_state['qwen_history'].append(mg.assistant_mesasage(full_response))



