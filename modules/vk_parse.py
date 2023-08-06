import vk_api

def get_group_items(group_id, access_token):
    # Авторизация в ВКонтакте с использованием токена группы
    vk_session = vk_api.VkApi(token=access_token)

    # Получение информации о товарах из группы
    vk = vk_session.get_api()
    albums = vk.market.getAlbums(owner_id=group_id)
    album_ids = [album['id'] for album in albums['items']]
    response = vk.market.get(owner_id=group_id, album_ids=album_ids, extended=1)

    # Обработка полученных данных
    items = []
    for item in response['items']:
        title = item['title']
        description = item['description']
        price = item['price']['text']
        photo_link = item['thumb_photo']
        
        # Добавление ссылки на товар
        link = f"https://vk.com/market{group_id}?w=product{group_id}_{item['id']}"
        item['link'] = link
        
        items.append({'title': title, 'description': description, 'price': price, 'photo_link': photo_link, 'link': link})
        # сохраняем: название товара, описание, цена, ссылка на главную миниатюру, ссылки на все фотки товара, ссылка на товар
    return items




