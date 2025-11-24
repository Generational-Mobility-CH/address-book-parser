import os

from dotenv import load_dotenv

from modules.shared.constants.paths import PROJECT_ROOT_PATH


def get_config_info():
    path = PROJECT_ROOT_PATH / ".env.local"
    load_dotenv(path)
    return {
        "selenium-web-driver-path": os.getenv("SELENIUM_WEB_DRIVER_PATH"),
        "openai-api-key": os.getenv("OPENAI_API_KEY"),
    }


class Config:
    __instance = None

    def __init__(self) -> None:
        if self.__initialized:
            return

        self.__initialized = True

        data = get_config_info()

        self.selenium_web_driver_path = os.path.join(
            os.getcwd(), str(data["selenium-web-driver-path"])
        )
        self.openai_api_key = data["openai-api-key"]

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def reload(self):
        self.__init__()
        return self


config_instance = Config()
