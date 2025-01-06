import streamlit as st
#st.title('首页')
pages = {
    "AI": [
        st.Page("./ai/ollama.py", title="ollama 测试"),
        #st.Page("manage_account.py", title="Manage your account"),
    ],
    "TOOLS": [
        st.Page("./tools/cal.py", title="计算器"),
        #st.Page("trial.py", title="Try it out"),
    ],
}

pg = st.navigation(pages)
pg.run()
