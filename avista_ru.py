import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_links_with_produkte(url, url_a):
    try:
        # Отправляем GET-запрос к сайту
        response = requests.get(url)
        response.raise_for_status()  # Проверяем на ошибки

        # Парсим HTML-контент
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим все ссылки на странице
        all_links = soup.find_all('a', href=True)

        # Фильтруем ссылки, содержащие "url_a"
        produkte_links = []
        for link in all_links:
            href = link['href']
            if url_a in href:
                # Преобразуем относительные ссылки в абсолютные
                absolute_url = urljoin(url, href)
                produkte_links.append(absolute_url)

        # Удаляем дубликаты
        unique_links = list(set(produkte_links))

        return unique_links

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к сайту: {e}")
        return []


# Пример использования
# website_url = "https://www.avista-lubes.de/produkte/"  # Замените на нужный URL
website_url = "https://www.avista-lubes.de/ru/produkty/"  # Замените на нужный URL
produkte_links = get_links_with_produkte(website_url, '/produkty/')

# product_ranges = []
#
# for link in produkte_links:
#     if link != website_url:
#         product_ranges.append(link)

prefinal_produkte_links = []

for link in produkte_links:
    temp = get_links_with_produkte(link, '/produkty/')
    for teml_l in temp:
        if "produkty/detal/avista" in teml_l and teml_l not in prefinal_produkte_links:
            prefinal_produkte_links.append(teml_l)

with open('linklist_ru.txt', 'w', encoding="utf-8") as file:
    for item in prefinal_produkte_links:
        file.write(item)
        file.write('\n')

with open('avista_ru.txt', 'w', encoding="utf-8") as file:
    pass

for url in prefinal_produkte_links:
    response = requests.get(url)
    response.raise_for_status()  # Проверяем на ошибки

    # Парсим HTML-контент
    soup = BeautifulSoup(response.text, 'html.parser')

    # Находим название продукта на странице
    product_name = soup.find('h1').text.encode('utf-8').decode('utf-8')

    product_description = soup.find('div', class_="producttext")
    if product_description:
        product_description = product_description.text.replace('\t', ' ').replace('\n', ' ').replace('\r', ' ').encode('utf8').decode('utf-8')
    else:
        product_description = 'нет описания'

    # Находим все данные на странице
    product_table = soup.find('div', class_=lambda x: x and x.strip() == 'sizes')

    soup = product_table

    # Находим все div-блоки с размерами (они имеют классы bulk, literXXXX и т.д.)
    size_blocks = soup.find_all('div', class_=lambda x: x and (
            'bulk' in x or
            'liter' in x or
            'tooltip_ext' in x or
            x.startswith('liter')
    ))

    results = []

    for block in size_blocks:
        # Извлекаем название размера из класса
        size_class = ' '.join([c for c in block.get('class', []) if c != 'noorder'])
        size_name = size_class.replace('liter', '').replace('bulk', 'lose Ware').strip()

        # Проверяем доступность товара
        available = 'noorder' not in block.get('class', [])

        # Извлекаем все данные из блока
        data = {
            'фасовка:': None,
            'артикул:': None,
            'EAN': None,
            'кратность:': None,
            'Available': available
        }

        # Парсим каждое поле

        new_tmp = []

        for p in block.find_all('p'):
            small = p.find('small')
            if small:
                key = small.get_text(strip=True).replace(':', '').strip()

                # Получаем значение
                if p.find('span'):
                    value = p.find('span').get_text(strip=True)
                else:
                    value = small.next_sibling.strip() if small.next_sibling else ""
                new_tmp.append(value)
                data[key] = value

        if data['Available'] == available:
            with open('avista_ru.txt', 'a', encoding="utf-8") as file:
                file.write(product_name)
                file.write('\t')
            with open('avista_ru.txt', 'a', encoding="utf-8") as file:
                for item in new_tmp:
                    try:
                        file.write(item)
                    except:
                        print(item)
                        pass
                    file.write('\t')
                file.write('\t')
                file.write(product_description)
                file.write('\n')
