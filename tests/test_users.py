import pytest
import json
import os
from selenium.webdriver.common.keys import Keys
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options
from subprocess import run
from time import sleep
from faker import Faker
from resource import (
    add_accept_header,
    add_content_type_header,
    increasing_request_response_timeout,
    wait_for_result_element_and_close_ad,
    wait_until_element_visible,
    log_in_user,
    delete_user,
    delete_json_file
)

@pytest.fixture
def driver():
    # Configurações do Appium
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

    driver = webdriver.Remote(command_executor="http://localhost:4723", options=options)
    yield driver
    driver.quit()

def test_create_user_account(driver):
    # Gerando dados aleatórios para o usuário
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    user_name = Faker().name()
    user_email = Faker().lexify(text='??').lower() + Faker().company_email().replace("-", "")
    user_password = Faker().password(length=12, special_chars=False, digits=True, upper_case=True, lower_case=True)

    # Desliga Wi-Fi
    run(["adb", "shell", "svc", "wifi", "disable"])

    sleep(5)

    # Aumenta os tempos de timeout
    increasing_request_response_timeout(driver)

    # Seleciona método HTTP (POST)
    sp_http_method = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod")
    sp_http_method.click()
    post_method = wait_until_element_visible(driver, AppiumBy.XPATH, "//android.widget.CheckedTextView[@resource-id='android:id/text1' and @text='POST']")
    post_method.click()

    # Insere URL base
    url_input = wait_until_element_visible(driver, AppiumBy.XPATH, "//android.widget.EditText[@resource-id='com.ab.apiclient:id/etUrl']")
    url_input.send_keys("https://practice.expandtesting.com/notes/api/users/register")

    # Adiciona headers
    add_accept_header(driver)
    add_content_type_header(driver)

    # Localiza o campo de entrada JSON
    json_input_field = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/etJSONData")

    # Prepara o corpo JSON com os dados das variáveis
    json_body = f'''{{
        "name": "{user_name}",
        "email": "{user_email}",
        "password": "{user_password}"
    }}'''

    # Insere o texto formatado no campo
    json_input_field.send_keys(json_body)

    # Envia requisição
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # Abre aba "Raw" para ver resultado
    raw_button = wait_until_element_visible(driver, AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")')
    raw_button.click()

    # Espera pelo resultado e fecha ad se necessário
    wait_for_result_element_and_close_ad(driver)

    # Captura o texto da resposta
    response_text_element = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/tvResult")
    response_str = response_text_element.text
    print(f"string response is: {response_str}")

    # Processa o JSON da resposta
    response_json = json.loads(response_str)

    success = response_json.get("success")
    status = response_json.get("status")
    message = response_json.get("message")

    # Asserts
    assert success is True
    assert str(status) == "201"
    assert message == "User account created successfully"

    # Criação do arquivo .json
    with open(f"tests/fixtures/testdata-{random_number}.json", "w") as f:
        json.dump({
            "user_email": user_email,
            "user_id": response_json['data']['id'],
            "user_name": user_name,
            "user_password": user_password
        }, f)

    # Pressiona a tecla "voltar" para voltar ao início e criar uma nova requisição
    driver.press_keycode(4)
    wait_until_element_visible(driver, AppiumBy.XPATH, "//android.widget.ImageButton")
    driver.find_element(AppiumBy.XPATH, "//android.widget.ImageButton").click()
    wait_until_element_visible(driver, AppiumBy.XPATH, "//android.widget.CheckedTextView[@resource-id='com.ab.apiclient:id/design_menu_item_text' and @text='New Request']")
    driver.find_element(AppiumBy.XPATH, "//android.widget.CheckedTextView[@resource-id='com.ab.apiclient:id/design_menu_item_text' and @text='New Request']").click()


    log_in_user(driver, random_number)
    delete_user(driver, random_number)

    sleep(5)

    delete_json_file(random_number)