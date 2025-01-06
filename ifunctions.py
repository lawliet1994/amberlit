import streamlit as st
import requests,sys
class Message:
    def __init__(self):
        pass
    def user_mesasage(self,content):
        response = {"role": "user", "content": content}
        return response
    def system_mesasage(self,content):
        response = {"role": "system", "content": content}
        return response
    def assistant_mesasage(self,content):
        response = {"role": "assistant", "content": content}
        return response

class Baidu:
    def __init__(self,API_KEY=st.secrets.baidu.API_KEY):
        self.API_KEY = API_KEY
    def get_weather(self,district_id):
        # 接口地址
        url = "https://api.map.baidu.com/weather/v1/"
        params = {
            "district_id":    district_id,
            "data_type":    "all",
            "ak":       self.API_KEY,
        }
        response = requests.get(url=url, params=params)
        if response:
            print(response.json())
        return response