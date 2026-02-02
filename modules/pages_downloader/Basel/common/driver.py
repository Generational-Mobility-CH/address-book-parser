from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from modules.shared.common.config import config_instance


def build_chrome_options(headless: bool = True) -> Options:
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"

    default_options = Options()

    if headless:
        default_options.add_argument("--headless=new")

    default_options.add_argument("--disable-gpu")
    default_options.add_argument("--no-sandbox")
    default_options.add_argument("--disable-dev-shm-usage")
    default_options.add_argument(f"user-agent={user_agent}")
    return default_options


def get_web_driver(headless: bool = True) -> webdriver.Chrome:
    options = build_chrome_options(headless)
    return webdriver.Chrome(
        service=Service(config_instance.selenium_web_driver_path), options=options
    )
