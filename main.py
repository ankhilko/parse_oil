import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_links_with_produkte(url):
    try:
        # Отправляем GET-запрос к сайту
        response = requests.get(url)
        response.raise_for_status()  # Проверяем на ошибки

        # Парсим HTML-контент
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим все ссылки на странице
        all_links = soup.find_all('a', href=True)

        # Фильтруем ссылки, содержащие "/produkte/"
        produkte_links = []
        for link in all_links:
            href = link['href']
            if "/produkte/" in href:
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
website_url = "https://www.avista-lubes.de/produkte/"  # Замените на нужный URL
produkte_links = get_links_with_produkte(website_url)

# product_ranges = []
#
# for link in produkte_links:
#     if link != website_url:
#         product_ranges.append(link)

prefinal_produkte_links = []

for link in produkte_links:
    temp = get_links_with_produkte(link)
    for teml_l in temp:
        if "produkte/detail/avista" in teml_l and teml_l not in prefinal_produkte_links:
            prefinal_produkte_links.append(teml_l)

with open('linklist.txt', 'w') as file:
    for item in prefinal_produkte_links:
        file.write(item)
        file.write('\n')


for url in prefinal_produkte_links:
    response = requests.get(url)
    response.raise_for_status()  # Проверяем на ошибки

    # Парсим HTML-контент
    soup = BeautifulSoup(response.text, 'html.parser')

    # Находим название продукта на странице
    product_name = soup.find('h1').text

    print(product_name)

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
            'Gebindegrößen': None,
            'ART. - NR': None,
            'EAN': None,
            'VE': None,
            'Available': available
        }

        # Парсим каждое поле

        new_tmp = []

        for p in block.find_all('p'):
            small = p.find('small')
            if small:
                key = small.get_text(strip=True).replace(':', '').strip()

                print(key, end='\t')

                # Получаем значение
                if p.find('span'):
                    value = p.find('span').get_text(strip=True)
                else:
                    value = small.next_sibling.strip() if small.next_sibling else ""

                print(value, end='\t')

                new_tmp.append(value)

                data[key] = value
        print()

        if data['Available'] == available:
            with open('avista.txt', 'a') as file:
                file.write(product_name)
                file.write('\t')
            with open('avista.txt', 'a') as file:
                for item in new_tmp:
                    try:
                        file.write(item)
                    except:
                        pass
                    file.write('\t')
                file.write('\n')
