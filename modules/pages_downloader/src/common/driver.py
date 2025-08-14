from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


# setup options to allow driver to run without opening chrome windows
default_options = webdriver.ChromeOptions()
default_options.add_argument("--headless=new")
default_options.add_argument("--disable-gpu")
default_options.add_argument("--no-sandbox")
default_options.add_argument("--disable-dev-shm-usage")
default_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
)

service = Service(
    "C:/Users/narman/Downloads/chromedriver-win64(1)/chromedriver-win64/chromedriver.exe"
)  # TODO: Add possibility to set path to chromedriver (for example via environment variable or config file)


def get_web_driver(options: Options = default_options) -> webdriver.Chrome:
    return webdriver.Chrome(service=service, options=options)
