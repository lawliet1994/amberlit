import streamlit as st
import sys
from ifunctions import Baidu
st.set_page_config(layout='wide')
baidu = Baidu(st.secrets.baidu.API_KEY)
st.title("Homepage")

weather = baidu.get_weather(district_id=310100).json()

# st.write(weather['result']['location'])
# st.write(weather['result']['now'])
# st.write(weather['result']['forecasts'])

st.html("""    
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>天气卡片</title>
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #f0f8ff;
            margin: 0;
            font-family: Arial, sans-serif;
        }
        .weather-card {
            background-color: #ffffff;
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            padding: 20px;
            text-align: center;
            width: 300px;
        }
        .weather-icon {
            font-size: 48px;
            color: #333;
        }
        .temperature {
            font-size: 36px;
            margin: 10px 0;
        }
        .details {
            font-size: 18px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="weather-card">
        <div class="weather-icon">☀️</div>
        <div class="temperature">7°C</div>
        <div class="details">
            <p>体感温度: 6°C</p>
            <p>湿度: 62%</p>
            <p>风速: 1级 东北风</p>
            <p>更新时间: 2025-01-06 21:40</p>
        </div>
    </div>
</body>
</html>     
        
        """)
