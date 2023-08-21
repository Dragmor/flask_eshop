from flask import Flask, render_template
from jinja2 import Environment, FileSystemLoader
import datetime
import asyncio
#
import modules.db_manager as db_manager

app = Flask(__name__)
app.debug = True

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port="80")
