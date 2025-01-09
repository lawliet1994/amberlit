import streamlit as st
import sys
from ifunctions import Baidu
from jinja2 import Template
import streamlit.components.v1 as components
import datetime
import sqlite3

#st.set_page_config(layout='wide')
baidu = Baidu(st.secrets.baidu.API_KEY)
with st.container():
    #st.markdown('hello world!')
    html_christmas = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Merry Christmas Card</title>
        <style>
            body {
                /* background-color: #ffebf5;*/
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .card {
                width: 350px;
                height: 500px;
                background-color: white;
                border-radius: 15px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                position: relative;
                overflow: hidden;
                padding: 20px;
                box-sizing: border-box;
            }
            .title, .content {
                text-align: center;
                color: black;
                font-family: 'Courier New', Courier, monospace;
            }
            .title {
                font-size: 24px;
                margin-bottom: 20px;
            }
            .content {
                font-size: 18px;
                margin-top: 20px;
            }
            img {
                width: 250px;
                height: auto;
                margin-bottom: 20px;
            }
            .emoji {
                position: absolute;
                font-size: 24px;
                animation: fall 2s linear forwards, slide 2s 2s linear forwards, fadeOut 2s 4s linear forwards;
            }
            @keyframes fall {
                from { transform: translateY(0); }
                to { transform: translateY(300px); }
            }
            @keyframes slide {
                from { transform: translateX(0); }
                to { transform: translateX(100px); }
            }
            @keyframes fadeOut {
                from { opacity: 1; }
                to { opacity: 0; }
            }
        </style>
    </head>
    <body>
        <div class="card">
            <div class="title" id="title"></div>
            <img src="https://modelscope.oss-cn-beijing.aliyuncs.com/resource/MerryQwristmas.png" alt="Christmas Tree">
            <div class="content" id="name"></div>
            <div class="content" id="content"></div>
        </div>

        <script>
            const titleText = "Merry Christmas!";
            const nameText = "诗谣！Click me！";
            const contentText = "May the holidays fill your heart with happiness";
            const titleElement = document.getElementById('title');
            const nameElement = document.getElementById('name');
            const contentElement = document.getElementById('content');

            function typeWriter(element, text, speed) {
                let i = 0;
                const interval = setInterval(() => {
                    if (i < text.length) {
                        element.innerHTML += text.charAt(i);
                        i++;
                    } else {
                        clearInterval(interval);
                    }
                }, speed);
            }

            typeWriter(titleElement, titleText, 150);
            typeWriter(nameElement, nameText, 250);
            typeWriter(contentElement, contentText, 100);

            document.querySelector('.card').addEventListener('click', (e) => {
                const emojis = ['🎄', '❄️'];
                const numEmojis = Math.floor(Math.random() * 5) + 3;

                for (let i = 0; i < numEmojis; i++) {
                    const emoji = document.createElement('div');
                    emoji.classList.add('emoji');
                    emoji.style.left = `${e.clientX - 5}px`; // Center the emoji based on card width
                    emoji.textContent = emojis[Math.floor(Math.random() * emojis.length)];
                    document.body.appendChild(emoji);

                    emoji.addEventListener('animationend', () => {
                        emoji.remove();
                    });
                }
            });
        </script>
    </body>
    </html>
    """
    components.html(html_christmas,height=600)
#st.title("Homepage")
main_col1,main_col2,main_col3 = st.columns([1,1,1],vertical_alignment='top')
with main_col1.container(height=400):
    weather = baidu.get_weather(district_id=310100).json()

    # st.write(weather['result']['location'])
    # st.write(weather['result']['now'])
    # st.write(weather['result']['forecasts'])
    #st.write(weather['result']['now'])
    html_str = """    
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
                {# background-color: #f0f8ff; #}
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
            <div class="weather-icon">{{weather_icon}}</div>
            <div class="temperature">7°C</div>
            <div class="details">
                <p>体感温度: {{temp}}°C</p>
                <p>湿度: {{rh}}%</p>
                <p>风速: {{wind_class}} {{wind_dir}}</p>
                <!-- <p>更新时间: {{update_time}}</p> -->
            </div>
        </div>
    </body>
    </html>     
            
            """
    html_temp = Template(html_str)
    if '晴' in weather['result']['now']['text']:
        temp_icon = '☀️'
    elif '阴' in weather['result']['now']['text']:
        temp_icon = '☁️'
    elif '雨' in weather['result']['now']['text']:
        temp_icon = '🌧️'
    elif '雪' in weather['result']['now']['text']:
        temp_icon = '❄️'
    elif '云' in weather['result']['now']['text']:
        temp_icon = '☁️'
    html_final = html_temp.render(
                                weather_icon=temp_icon,      
                                temp=weather['result']['now']['temp'],
                                rh=weather['result']['now']['rh'],
                                wind_class=weather['result']['now']['wind_class'],
                                wind_dir=weather['result']['now']['wind_dir'],
                                update_time=(weather['result']['now']['uptime']))
    components.html(html_final, height=350)
with main_col2.container(height=400):
    def get_todo_list():
        # 使用sqlite3 创建数据库并创建一个todo list的表，包括三个字段：id和content和status
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS todo_list (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                content TEXT NOT NULL,
                                status BOOLEAN DEFAULT 0
                            )''')
            all_data = cursor.execute('''SELECT * FROM todo_list''')
            todo_list = [{'id': row[0], 'content': row[1], 'status': row[2]} for row in all_data.fetchall()]
            #st.write(todo_list)
            return todo_list
    def update_status(id):
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''UPDATE todo_list SET status = 1 WHERE id = ?''', (id,))
            conn.commit()
    def add_new_task(new_task):
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO todo_list (content) VALUES (?)''', (new_task,))
            conn.commit()
    #col1,col2 = st.columns([1,1],vertical_alignment='top')
    st.title('TODO LIST')
    new_task = st.text_input('Add a new task')
    if st.button('Add'):
        add_new_task(new_task)
    #col2.markdown('### To Do List')
with main_col3.container(height=400):
    for item in get_todo_list():
        if item['status'] == 0:
            if st.checkbox(item['content'], key=item['id']):
                update_status(item['id'])
            #st.divider()
            #st.rerun()

    



