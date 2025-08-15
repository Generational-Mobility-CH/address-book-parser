from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from modules.shared.config import config_instance


default_options = webdriver.ChromeOptions()
default_options.add_argument("--headless=new")
default_options.add_argument("--disable-gpu")
default_options.add_argument("--no-sandbox")
default_options.add_argument("--disable-dev-shm-usage")
default_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
)


def get_web_driver(options: Options = default_options) -> webdriver:
    return webdriver.Chrome(
        service=Service(config_instance.selenium_web_driver_path), options=options
    )
