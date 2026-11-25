import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait



class Methods():
    def __init__(self, mode):
        # тут конфигурируем драйвер в зависимости от режима десктоп/мобилка (desk/mob)
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless=new') #режим со скрытым браузером
        self.chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
        if mode == "desk":
            self.driver = webdriver.Chrome(options=self.chrome_options)
        elif mode == "mob":
            self.mobile_emulation = {"deviceName": "Samsung Galaxy S20 Ultra"}
            self.chrome_options.add_experimental_option("mobileEmulation", self.mobile_emulation)
            self.driver = webdriver.Chrome(options=self.chrome_options)
        # дополнительные режимы деск/моб с отключением ошибок cors и сертификатов (если например на ст настроено ифтшное апи)
        elif mode == "desk_cors":
            # --- БЛОК: ОТКЛЮЧЕНИЕ CORS ---
            # --disable-web-security отключает Same Origin Policy (CORS)
            self.chrome_options.add_argument("--disable-web-security")
            # Часто вместе с CORS нужно отключить изоляцию сайтов
            self.chrome_options.add_argument("--disable-site-isolation-trials")
            # Важно: для работы --disable-web-security в новых версиях Chrome
            # иногда требуется указать путь к временной папке профиля пользователя
            # пока работает и без этого
            #self.chrome_options.add_argument("--user-data-dir=/tmp/chrome_test_profile")
            # Игнорировать ошибки SSL
            self.chrome_options.add_argument("--ignore-certificate-errors")
            self.driver = webdriver.Chrome(options=self.chrome_options)
        elif mode == "mob_cors":
            self.mobile_emulation = {"deviceName": "Samsung Galaxy S20 Ultra"}
            self.chrome_options.add_experimental_option("mobileEmulation", self.mobile_emulation)
            self.chrome_options.add_argument("--disable-web-security")
            self.chrome_options.add_argument("--disable-site-isolation-trials")
            self.chrome_options.add_argument("--ignore-certificate-errors")
            self.driver = webdriver.Chrome(options=self.chrome_options)

    def open_page(self, link_page):
        # Открытие страницы
        self.driver.get(link_page)
        print("Страница Открыта")

        # Залипание 2 секунды
        #time.sleep(3)
        #print("Залипание 3 сек выполнено")

        # Явное ожидание элемента на 10 сек
        wait = WebDriverWait(self.driver, 10)
        # Ожидание корневого div, в котором лежат все компоненты на странице
        element = wait.until(ec.visibility_of_element_located((By.ID, "root")))

        # Проверка на найденный элемент (если проверка не прошла, тест упадет)
        assert element is not None, "Ошибка - корневой элемент DOM div с id=root не оказался видимым"

    # доп. метод для подборщика вкладов и нс
    def wait_element_for_calc_picker(self):
        # Явное ожидание элемента на 10 сек
        wait = WebDriverWait(self.driver, 10)
        # Ожидание
        element_rate = wait.until(ec.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'Накопительный счёт')]")))
        assert element_rate is not None, "Ошибка - чипс Накопительный счет не оказался видимым'"

    def check_log_browser(self):
        try:
            # подключаемся к логу браузера
            browser_logs = self.driver.get_log('browser')

            # Фильтрация и вывод ошибок
            print("Проверка консоли браузера:")
            errors_found = False
            error_message = None
            for log in browser_logs:
                # Уровни логов: SEVERE (ошибки), WARNING, INFO, DEBUG. Мы смотрим только SEVERE
                if log['level'] == 'SEVERE':
                    print(f"ERROR: {log['timestamp']} - {log['source']} - {log['message']}")
                    # отлавливание ошибок Minified React error и source javascript
                    if "Minified React error #" in log['message'] and log['source'] == "javascript":
                        errors_found = True
                        error_message = log['message']
            if not errors_found:
                print("Ошибок уровня SEVERE (ERROR) не обнаружено.")
            assert not errors_found, "Возникли ошибки React " + error_message
        finally:
            self.driver.quit()

