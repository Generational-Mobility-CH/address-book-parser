import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.wait import WebDriverWait

WAIT_TIME = 30


def click_btn(driver, btn_string):
    wait = WebDriverWait(driver, WAIT_TIME)
    xpath_button = f"//button[contains(@class,'tify-header-button') and contains(@aria-controls,'{btn_string}')]"
    xpath_link = f"//section[contains(@class,'tify-export')]//a[contains(normalize-space(),'{btn_string}')]"
    btn = wait.until(
        EC.any_of(
            EC.presence_of_element_located((By.XPATH, xpath_button)),
            EC.presence_of_element_located((By.XPATH, xpath_link)),
        )
    )

    driver.execute_script("arguments[0].scrollIntoView(true);", btn)
    time.sleep(0.5)

    driver.execute_script("arguments[0].click();", btn)
    time.sleep(1)
