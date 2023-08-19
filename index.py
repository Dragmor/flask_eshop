from jinja2 import Template, Environment, FileSystemLoader
from flask import Flask, render_template
from gevent.pywsgi import WSGIServer
import asyncio
import time
import datetime
import os
import multiprocessing
#
import modules.db_manager as db_manager
import modules.vk_parse as vk_parse

app = Flask(__name__)
app.debug = True

def parser_process(token):
    # процесс, который парсит из группы ВК товары, и загружает их в БД
    if token:
        print("Парсер запущен с токеном")
    else:
        print("Токен не был передан в парсер!")
        return
    while True:
        try:
            # парсим из группы вк товары
            group_id = -220392532  # Замените на ID вашей группы
            access_token = token  # Замените на ваш токен группы
            try:
                cards = vk_parse.get_group_items(group_id, access_token)
            except Exception as error:
                print(f"Ошибка при получении товаров из группы: {error}")
                time.sleep(300)
                continue
            if not cards:
                print("В группе не обнаружено товаров!")
                time.sleep(300)
                continue
            # записываем в БД все товары, которые спарсили
            asyncio.run(db_manager.write_items_to_database(cards))  
        except Exception as error:
            print(f"Ошибка загрузки товаров из группы: {error}")
            time.sleep(300)
        else:
            print("Товары из группы загружены!")
            time.sleep(3600) # ждём час

@app.route('/')
def index():
    current_year = datetime.datetime.now().year
    formatted_year = str(current_year)

    variables = {
                "site_name":"Саженцы-Крым",
                "title":"Саженцы-Крым",
                "site_description":"Саженцы туй, можжевельников и прочих декоративных растений в Нижнегорске",                
                "description":"Добро пожаловать на наш сайт-визитку, специализирующийся на продаже высококачественных хвойных саженцев и роз. Мы предлагаем широкий ассортимент сортов, подходящих для различных климатических условий. Наша команда опытных садоводов гарантирует, что каждый саженец выращен с заботой и вниманием к деталям.",
                "keywords":"хвойные саженцы, розы, продажа саженцев, садоводство, ландшафтный дизайн, растения для сада, сорта хвойных растений, сорта роз, купить саженцы, садовые растения, садовый центр",
                "footer_text":f"Саженцы-Крым.рф 2023-{formatted_year}"
                }  


    

    # группируем карточки товаров на 3 группы
    cards_group_1 = asyncio.run(db_manager.get_cards(1)) 
    cards_group_2 = asyncio.run(db_manager.get_cards(2)) 
    cards_group_3 = asyncio.run(db_manager.get_cards(3))
    
    # Загрузка шаблона из файла
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('templates/cards_block.html')

    # Данные для каждого блока
    data = [
        {
            'section_title': 'Туи',
            'container_id': 'card-container-1',
            'cards': cards_group_1
        },
        {
            'section_title': 'Можжевельники',
            'container_id': 'card-container-2',
            'cards': cards_group_2
        },
        {
            'section_title': 'Прочие растения',
            'container_id': 'card-container-3',
            'cards': cards_group_3
        }
    ]
    # создаём кусок кода для блоков с карточками
    html_blocks = []
    for block_data in data:
        html_block = template.render(block_data)
        html_blocks.append(html_block)

    # Объединение сгенерированных блоков в один HTML-код
    card_blocks = '\n'.join(html_blocks)

    return render_template('index.html', card_blocks=card_blocks, **variables)

if __name__ == '__main__':
    token = os.getenv('VK_TOKEN')
    parser = multiprocessing.Process(target=parser_process, args=(token,))
    parser.start()

    http_server = WSGIServer(('0.0.0.0', 8080), app)
    http_server.serve_forever()






'''
import logging

# Создание и настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Создание обработчика для вывода логов в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Создание форматтера для определения формата вывода логов
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Добавление обработчика к логгеру
logger.addHandler(console_handler)

# Пример использования логгера
def parser_process(token):
    # ...
    while True:
        try:
            # ...
        except Exception as error:
            logger.error(f"Ошибка загрузки товаров из группы: {error}")
            time.sleep(300)
        else:
            logger.info("Товары из группы загружены!")
            time.sleep(3600) # ждём час

if __name__ == '__main__':
    # ...

В этом примере, логгер создается с именем модуля (__name__) и устанавливается уровень логирования на DEBUG. Затем создается обработчик для вывода логов в консоль, устанавливается уровень логирования на DEBUG и применяется форматтер для определения формата вывода логов. Обработчик добавляется к логгеру, и теперь вы можете использовать логгер для записи логов в разных частях вашего кода, например, с помощью logger.error() или logger.info().
Помимо вывода логов в консоль, вы также можете настроить логгер для записи логов в файл или другие места.

GPT-3.5
'''