from flask import Flask, render_template
from jinja2 import Template, Environment, FileSystemLoader
import datetime
import asyncio
import time
#
import modules.db_manager as db_manager
import modules.vk_parse as vk_parse

app = Flask(__name__)
app.debug = True

def parser_process(token=None):
    # процесс, который парсит из группы ВК товары, и загружает их в БД
    if token:
        print("Ok! Running with token")
    else:
        print("Run without token!")
        return
    while True:
        try:
            # парсим из группы вк товары
            group_id = -220392532  # Замените на ID вашей группы
            access_token = token  # Замените на ваш токен группы
            try:
                cards = vk_parse.get_group_items(group_id, access_token)
            except Exception as error:
                print(f"Parsing product error: {error}")
                time.sleep(300)
                continue
            if not cards:
                print("Can't find products in VK group!")
                time.sleep(300)
                continue
            # записываем в БД все товары, которые спарсили
            asyncio.run(db_manager.write_items_to_database(cards))  
        except Exception as error:
            print(f"Loading products error: {error}")
            time.sleep(300)
        else:
            print("Ok! Products loading complete!")
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
                "footer_text":f"Хвоя-Крым.рф 2023-{formatted_year}"
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

# if __name__ == '__main__':
#     token = os.getenv('VK_TOKEN')
#     parser = multiprocessing.Process(target=parser_process, args=(token,))
#     parser.start()

#     http_server = WSGIServer(('0.0.0.0', 8080), app)
#     http_server.serve_forever()
