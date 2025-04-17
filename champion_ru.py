from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import csv
import time
from pprint import pprint

PRODUCT_URL_ADD = '#sizes-and-packaging'


# Настройка Chrome для отключения загрузки изображений
chrome_options = webdriver.ChromeOptions()
prefs = {
    "profile.managed_default_content_settings.images": 2,  # Отключаем изображения
    "profile.default_content_setting_values.stylesheet": 2,  # Опционально: отключаем CSS
}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=chrome_options)

start_url = "https://www.championlubes.com/en-us"
start_url = "https://by.championlubes.com/ru-ru/"

try:
    # Открываем страницу продукта
    print("Открываем страницу: " + start_url)
    driver.get(start_url)

    # Принимаем куки, если есть
    try:
        cookie_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
        cookie_btn.click()
        # print("Куки приняты")
        time.sleep(0.5)
    except (NoSuchElementException, TimeoutException):
        print("Кнопка куки не найдена")
        pass

    try:
        close_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.c-dialog__btn-close[data-a11y-dialog-hide]"))
        )
        close_button.click()
        # print("Кнопка закрытия успешно нажата")
    except TimeoutException:
        print("Кнопка закрытия не найдена в течение 10 секунд")
    except NoSuchElementException:
        print("Элемент кнопки закрытия не существует на странице")
    except Exception as e:
        print(f"Произошла ошибка при клике: {str(e)}")
except Exception as e:
    print(f"Ошибка: {str(e)}")

products_tabs = [
    'https://by.championlubes.com/ru-ru/products/%D0%BB%D0%B5%D0%B3%D0%BA%D0%BE%D0%B2%D1%8B%D0%B5-%D0%B0%D0%B2%D1%82%D0%BE%D0%BC%D0%BE%D0%B1%D0%B8%D0%BB%D0%B8',
    'https://by.championlubes.com/ru-ru/products/%D0%B3%D1%80%D1%83%D0%B7%D0%BE%D0%B2%D0%B0%D1%8F-%D1%82%D0%B5%D1%85%D0%BD%D0%B8%D0%BA%D0%B0',
    'https://by.championlubes.com/ru-ru/products/%D0%B2%D0%BD%D0%B5%D0%B4%D0%BE%D1%80%D0%BE%D0%B6%D0%BD%D0%B0%D1%8F-%D1%82%D0%B5%D1%85%D0%BD%D0%B8%D0%BA%D0%B0',
    'https://by.championlubes.com/ru-ru/products/%D1%81%D0%B5%D0%BB%D1%8C%D1%81%D0%BA%D0%BE%D0%B5-%D1%85%D0%BE%D0%B7%D1%8F%D0%B8%D1%81%D1%82%D0%B2%D0%BE',
    'https://by.championlubes.com/ru-ru/products/%D1%81%D0%B0%D0%B4%D0%BE%D0%B2%D0%B0%D1%8F-%D1%82%D0%B5%D1%85%D0%BD%D0%B8%D0%BA%D0%B0',
    'https://by.championlubes.com/ru-ru/products/%D0%BC%D0%BE%D1%82%D0%BE%D1%86%D0%B8%D0%BA%D0%BB%D1%8B-%D0%B8-%D0%BA%D0%B2%D0%B0%D0%B4%D1%80%D0%BE%D1%86%D0%B8%D0%BA%D0%BB%D1%8B',
    'https://by.championlubes.com/ru-ru/products/%D0%BF%D1%80%D0%BE%D0%BC%D1%8B%D1%88%D0%BB%D0%B5%D0%BD%D0%BD%D0%BE%D1%81%D1%82%D1%8C',
    'https://by.championlubes.com/ru-ru/products/%D0%B2%D0%BE%D0%B4%D0%BD%D1%8B%D0%B8-%D1%82%D1%80%D0%B0%D0%BD%D1%81%D0%BF%D0%BE%D1%80%D1%82',
    'https://by.championlubes.com/ru-ru/products/%D0%B4%D1%80%D1%83%D0%B3%D0%BE%D0%B5'
]
items_500 = '?pageSize=500'

urls = []

with open('champion.txt', 'w', newline='', encoding='utf-8') as f:
    f.write('')

for tab in products_tabs:
    url = tab + items_500
    driver.get(url)

    def get_all_links(url1, driver1):

        # Получаем начальную высоту страницы
        last_height = driver1.execute_script("return document.body.scrollHeight")

        # Прокручиваем страницу до конца
        while True:
            # Прокрутка вниз
            driver1.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Ждем загрузки контента
            time.sleep(2)

            # Получаем новую высоту страницы
            new_height = driver.execute_script("return document.body.scrollHeight")

            # Если высота не изменилась - выходим из цикла
            if new_height == last_height:
                break
            last_height = new_height

        # Собираем все элементы ссылок
        links1 = driver.find_elements(By.TAG_NAME, 'a')

        # Извлекаем атрибуты href
        hrefs = [link1.get_attribute('href') for link1 in links1 if link1.get_attribute('href')]
        return hrefs


    # Пример использования
    all_links = get_all_links(url, driver)

    # Выводим найденные ссылки
    for i, link in enumerate(all_links, 1):
        if '/champion-' in link and link not in 'https://www.linkedin.com/showcase/champion-lubricants/' and link not in urls:
            urls.append(link)
            with open('champion.txt', 'a') as file:
                file.write(link)
                file.write('\n')

with open('product_packaging.csv', 'w', newline='', encoding='utf-8') as f:
    f.write('')

all_items = []

for url in urls:

    try:
        # Открываем страницу продукта
        # print("Открываем страницу продукта: " + url)
        driver.get(url + PRODUCT_URL_ADD)

        current_item = {
            "Product": driver.find_element(By.TAG_NAME, "h1").text.strip().replace('\n', ' ').replace('  ', ' ')
        }

        description = driver.find_element(By.CLASS_NAME, "c-product-detail__description")
        if description:
            current_item["Description"] = description.text.strip().replace('\n', ' ').replace('  ', ' ')

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".c-product-sizes")))

        # Сбор данных
        # print("Собираем данные...")
        all_blocks = driver.find_elements(By.CSS_SELECTOR, ".c-product-sizes__container > div")

        for block in all_blocks:
            classes = block.get_attribute("class")

            if "c-product-sizes__size" in classes:
                if current_item:
                    current_item["Size:"] = block.find_element(By.CSS_SELECTOR, ".c-product-sizes__title").text.strip()
            elif "c-product-sizes__info-item" in classes:
                try:
                    label = block.find_element(By.CSS_SELECTOR, "small").text.strip()
                    if "Status" in label:
                        value = block.find_element(By.CSS_SELECTOR, ".c-product-sizes__status-value").text.strip()
                        current_item[label] = value
                        all_items.append(current_item)
                        current_item = {
                            "Product": driver.find_element(By.TAG_NAME, "h1").text.strip().replace('\n', ' ').replace(
                                '  ', ' ')
                        }
                    else:
                        value = block.find_element(By.CSS_SELECTOR, ".c-product-sizes__value").text.strip()

                    current_item[label if label else "Packaging"] = value
                except NoSuchElementException:
                    continue

    except Exception as e:
        print(f"Ошибка: ", url)

if all_items:
    keys = set().union(*(d.keys() for d in all_items))  # Все уникальные ключи
    with open('product_packaging.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(all_items)
    print(f"Данные сохранены в product_packaging.csv ({len(all_items)} записей)")
else:
    print("Данные не найдены")

driver.quit()
print("\nРабота завершена")
