import pytest
import json
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options  # Importando a opção correta
from subprocess import run
from time import sleep

from resource import (
    add_accept_header,
    increasing_request_response_timeout,
    wait_for_result_element_and_close_ad,
    wait_until_element_visible
)

@pytest.fixture
def driver():
    # Criando a opção usando UiAutomator2Options
    options = UiAutomator2Options()
    options.platform_name = "android"
    options.platform_version = "10.0"
    options.device_name = "Pixel_4_API_29"
    options.automation_name = "UIAutomator2"
    options.app = "./apps/apiClient.apk"
    options.adb_exec_timeout = 60000
    options.auto_grant_permissions = True
    options.app_activity = "com.ab.apiclient.ui.Splash"
    options.app_wait_activity = "com.ab.apiclient.ui.Splash,com.ab.apiclient.*,com.ab.apiclient.ui.MainActivity"
    options.app_wait_duration = 20000
    options.uiautomator2_server_install_timeout = 60000

    # github actions
    # driver = webdriver.Remote(command_executor="http://localhost:4723/wd/hub", options=options)
    driver = webdriver.Remote(command_executor="http://localhost:4723", options=options)
    #local
    yield driver
    driver.quit()

def test_check_api_health(driver):
    # Desliga Wi-Fi
    run(["adb", "shell", "svc", "wifi", "disable"])

    sleep(5)

    increasing_request_response_timeout(driver)

    # Input base URL
    url_input = wait_until_element_visible(driver, AppiumBy.XPATH, "//android.widget.EditText[@resource-id='com.ab.apiclient:id/etUrl']")
    url_input.send_keys("https://practice.expandtesting.com/notes/api/health-check")

    # Adiciona header Accept: application/xml
    add_accept_header(driver)

    # Envia requisição
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # Abre aba "Raw" para ver resultado
    wait_until_element_visible(driver, AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")').click()

    # Espera pelo resultado e fecha ad se necessário
    wait_for_result_element_and_close_ad(driver)

    # Captura texto da resposta
    response_text_element = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/tvResult")
    response_str = response_text_element.text
    print(f"string response is: {response_str}")

    # Processa JSON
    response_json = json.loads(response_str)

    success = response_json.get("success")
    status = response_json.get("status")
    message = response_json.get("message")

    # Asserts
    assert success is True
    assert str(status) == "200"
    assert message == "Notes API is Running"
