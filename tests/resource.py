from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TIMEOUT = 30

def wait_until_element_visible(driver: WebDriver, by, value, timeout=TIMEOUT):
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by, value)))

def add_accept_header(driver: WebDriver):
    wait_until_element_visible(driver, By.CLASS_NAME, "android.widget.ImageView").click()
    wait_until_element_visible(driver, By.ID, "com.ab.apiclient:id/iconDown").click()
    wait_until_element_visible(driver, By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Accept")').click()
    wait_until_element_visible(driver, By.ID, "com.ab.apiclient:id/iconDownVal").click()
    wait_until_element_visible(driver, By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("application/xml")').click()

def increasing_request_response_timeout(driver: WebDriver):
    wait_until_element_visible(driver, By.CLASS_NAME, "android.widget.ImageButton").click()
    wait_until_element_visible(driver, By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Settings")').click()

    wait_until_element_visible(driver, By.ID, "com.ab.apiclient:id/etTimeoutConnection").clear()
    driver.find_element(By.ID, "com.ab.apiclient:id/etTimeoutConnection").send_keys("120")

    wait_until_element_visible(driver, By.ID, "com.ab.apiclient:id/etTimeoutREAD").clear()
    driver.find_element(By.ID, "com.ab.apiclient:id/etTimeoutREAD").send_keys("120")

    wait_until_element_visible(driver, By.ID, "com.ab.apiclient:id/etTimeoutWRITE").clear()
    driver.find_element(By.ID, "com.ab.apiclient:id/etTimeoutWRITE").send_keys("120")

    wait_until_element_visible(driver, By.CLASS_NAME, "android.widget.ImageButton").click()
    wait_until_element_visible(driver, By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("New Request")').click()

def wait_for_result_element_and_close_ad(driver: WebDriver):
    try:
        wait_until_element_visible(driver, By.ID, "com.ab.apiclient:id/tvResult", timeout=20)
    except TimeoutException:
        close_full_screen_ad(driver)
        wait_until_element_visible(driver, By.ID, "com.ab.apiclient:id/tvResult", timeout=10)

def close_full_screen_ad(driver: WebDriver):
    # Implementar aqui conforme o comportamento do ad
    pass
