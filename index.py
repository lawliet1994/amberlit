import streamlit as st
import sys
#st.title('首页')
st.set_page_config(layout="wide")
pages = {
    "首页":[
        st.Page("./tools/homepage.py", title="🎉 首页"),    
    ],
    "AI": [
        st.Page("./ai/qwen_web.py", title="✨ 通义千问"),
        st.Page("./ai/ollama.py", title="✨ ollama 测试"),
        st.Page("./tools/structured_output.py", title="🧷 结构化测试"),
        #st.Page("manage_account.py", title="Manage your account"),
    ],
    "TOOLS": [
        st.Page("./tools/cal.py", title="🧮 计算器"),
        #st.Page("trial.py", title="Try it out"),
    ],
}
with st.sidebar:
    if st.text_input("key to use",type='password') == st.secrets.index.password:
        st.session_state['login_in'] = True
    else:
        st.session_state['login_in'] = False
if st.session_state['login_in']:
    pg = st.navigation(pages)
    pg.run()
