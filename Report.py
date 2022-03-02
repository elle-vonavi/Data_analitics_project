#Скрипт для ежедневной автоматической отправки аналитической сводки в корпоративный телеграм.
#В отчет включены основные метрики: 
#DAU 
#Просмотры
#Лайки
#CTR
#Количество постов
#Количество лайков на 1 пользователя

import pandas as pd
import telegram
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io 
import os

#Запрос для получения report_data.csv:
# SELECT toDate(time) as date,
#          uniqExact(user_id) as DAU, 
#          countIf(user_id, action = 'view') as views,
#          countIf(user_id, action = 'like') as likes,
#          likes / views * 100 as CTR,
#          uniqExact(post_id) as posts, 
#          likes / DAU as LPU
# FROM simulator_20220120.feed_actions 
# WHERE toDate(time) between today()-8 and today()-1
# GROUP BY date
# ORDER BY date

df = pd.read_csv('report_data.csv')

def feed_report(chat = None):
    chat_id = chat or 1271269759
    bot = telegram.Bot(token=os.environ.get('REPORT_BOT_TOKEN'))
    msg = f'''Основные метрики по ленте новостей за {df.date.iloc[-1]}:\
             DAU: {df.DAU.iloc[-1]}\
             Просмотры: {df.views.iloc[-1]}\
             Лайки: {df.likes.iloc[-1]}\
             CTR: {round(df.CTR.iloc[-1], 2)}%\
             Посты: {df.posts.iloc[-1]}\
             LPU: {round(df.LPU.iloc[-1])}'''
    bot.send_message(chat_id=chat_id, text=msg)
    
    
    
    fig, axes = plt.subplots(3, 2, figsize=(16, 12))
    plt.tight_layout(pad=4)
    plt.suptitle('Статистика по ленте новостей за последние 7 дней'')
    axes[0, 0].set_title('Уникальные пользователи')
    axes[0, 0].set_xlabel('Дата')
    sns.lineplot(df.date, df.DAU, ax=axes[0,0])
    axes[0,1].set_title('Количество постов')
    axes[0,1].set_xlabel('Дата')
    sns.lineplot(df.date, df.posts, ax=axes[0,1])
    axes[1,0].set_title('Просмотры')
    axes[1,0].set_xlabel('Дата')
    sns.lineplot(df.date, df.views, ax=axes[1,0])
    axes[1,1].set_title('Лайки')
    axes[1,1].set_xlabel('Дата')
    sns.lineplot(df.date, df.likes, ax=axes[1,1])
    axes[2,0].set_title('CTR')
    axes[2,0].set_xlabel('Дата')
    sns.lineplot(df.date, df.CTR, ax=axes[2,0])
    axes[2,1].set_title('Лайки на 1 пользователя')
    axes[2,1].set_xlabel('Дата')
    sns.lineplot(df.date, df.LPU, ax=axes[2,1]);

    plot_object = io.BytesIO()
    plt.savefig(plot_object) 
    plot_object.name = 'feed_plots.png' 
    plot_object.seek(0)
    plt.close()
    bot.send_photo(chat_id=chat_id, photo=plot_object)
        

try:
    feed_report()
except Exception as e:
    print(e)