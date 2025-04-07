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
website_url = "https://www.avista-lubes.de/produkte/"  # Замените на нужный URL
produkte_links = get_links_with_produkte(website_url)

product_ranges = []

for link in produkte_links:
    if link != website_url:
        product_ranges.append(link)

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


'''
div class="sizes "
"Gebindegrößen:"
"ART. - NR:"
"EAN:"
"VE:"
'''

def Product():
    volume = 'Gebindegrößen:'
    pnumber = 'ART. - NR:'
    ean = 'EAN:'
    ve = 'VE:'


