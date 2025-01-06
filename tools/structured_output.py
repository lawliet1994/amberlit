import streamlit as st
import sys,ollama
from pydantic import BaseModel
import json

o = ollama.Client(host=st.secrets.ollama.host)
st.title('Structured Output')
class person(BaseModel):
    name:str
    age:int
question = st.chat_input("question")
if question:
    with st.chat_message("user"):
        st.write(question)
    response = o.chat(
        model = st.secrets.ollama.model,
        messages= [
            {"role": "user", "content": question}
        ],
        format=person.model_json_schema()
        # stream=True,
        # stream_callback=lambda x: st.write(x)
    )
    with st.chat_message("assistant"):
        st.write(response.model_dump_json())
        st.write(json.loads(response.model_dump_json())['message'])

