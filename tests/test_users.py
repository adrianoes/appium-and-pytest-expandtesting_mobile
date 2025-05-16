import pytest
import json
import os
from selenium.webdriver.common.keys import Keys
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support import expected_conditions as EC
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
    delete_json_file, 
    create_user,
    add_token_header,
    add_token_header_unauthorized
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

    # github actions
    driver = webdriver.Remote(command_executor="http://localhost:4723/wd/hub", options=options)
    # driver = webdriver.Remote(command_executor="http://localhost:4723", options=options)
    #local
    yield driver
    driver.quit()

def test_create_user(driver):
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

def test_create_user_br(driver):
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
        "email": "@{user_email}",
        "password": "{user_password}"
    }}'''

    # Insere o texto formatado no campo
    json_input_field.send_keys(json_body)

    # Envia requisição
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # Abre aba "Raw" para ver resultado
    # raw_button = wait_until_element_visible(driver, AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")')
    # raw_button.click()

    # # Espera pelo resultado e fecha ad se necessário
    # wait_for_result_element_and_close_ad(driver)

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
    assert success is False
    assert str(status) == "400"
    assert message == "A valid email address is required"

def test_login_user(driver):
    # Gerando dados aleatórios para o usuário
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user(driver, random_number)

    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_email = data['user_email']
    user_password = data['user_password']
    user_id = data['user_id']
    user_name = data['user_name']

    wait = WebDriverWait(driver, 20)

    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="POST"]'))).click()

    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys("https://practice.expandtesting.com/notes/api/users/login")

    add_accept_header(driver)
    add_content_type_header(driver)

    # Localiza o campo de entrada JSON
    json_input_field = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/etJSONData")

    # Prepara o corpo JSON com os dados das variáveis
    json_body = f'''{{
        "email": "{user_email}",
        "password": "{user_password}"
    }}'''

    # Insere o texto formatado no campo
    json_input_field.send_keys(json_body)

    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")'))).click()
    wait_for_result_element_and_close_ad(driver)
    response_str = driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/tvResult").text
    response = json.loads(response_str)

    assert response["success"] is True
    assert str(response["status"]) == "200"
    assert response["message"] == "Login successful"
    assert response["data"]["id"] == user_id
    assert response["data"]["name"] == user_name
    assert response["data"]["email"] == user_email

    user_token = response["data"]["token"]
    data["user_token"] = user_token

    with open(filepath, 'w') as file:
        json.dump(data, file)

    driver.press_keycode(4)
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="com.ab.apiclient:id/design_menu_item_text" and @text="New Request"]'))).click()

    delete_user(driver, random_number)

    sleep(5)

    delete_json_file(random_number)

def test_login_user_br(driver):
    # Gerando dados aleatórios para o usuário
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user(driver, random_number)

    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_email = data['user_email']
    user_password = data['user_password']
    user_id = data['user_id']
    user_name = data['user_name']

    wait = WebDriverWait(driver, 20)

    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="POST"]'))).click()

    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys("https://practice.expandtesting.com/notes/api/users/login")

    add_accept_header(driver)
    add_content_type_header(driver)

    # Localiza o campo de entrada JSON
    json_input_field = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/etJSONData")

    # Prepara o corpo JSON com os dados das variáveis
    json_body = f'''{{
        "email": "@{user_email}",
        "password": "{user_password}"
    }}'''

    # Insere o texto formatado no campo
    json_input_field.send_keys(json_body)

    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")'))).click()
    # wait_for_result_element_and_close_ad(driver)
    response_text_element = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/tvResult")
    response_str = response_text_element.text
    response = json.loads(response_str)

    assert response["success"] is False
    assert str(response["status"]) == "400"
    assert response["message"] == "A valid email address is required"

    driver.press_keycode(4)
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="com.ab.apiclient:id/design_menu_item_text" and @text="New Request"]'))).click()

    log_in_user(driver, random_number)  

    delete_user(driver, random_number)

    sleep(5)

    delete_json_file(random_number)

def test_login_user_ur(driver):
    # Gerando dados aleatórios para o usuário
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user(driver, random_number)

    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_email = data['user_email']
    user_password = data['user_password']
    user_id = data['user_id']
    user_name = data['user_name']

    wait = WebDriverWait(driver, 20)

    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="POST"]'))).click()

    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys("https://practice.expandtesting.com/notes/api/users/login")

    add_accept_header(driver)
    add_content_type_header(driver)

    # Localiza o campo de entrada JSON
    json_input_field = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/etJSONData")

    # Prepara o corpo JSON com os dados das variáveis
    json_body = f'''{{
        "email": "{user_email}",
        "password": "@{user_password}"
    }}'''

    # Insere o texto formatado no campo
    json_input_field.send_keys(json_body)

    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")'))).click()
    # wait_for_result_element_and_close_ad(driver)
    response_text_element = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/tvResult")
    response_str = response_text_element.text
    response = json.loads(response_str)

    assert response["success"] is False
    assert str(response["status"]) == "401"
    assert response["message"] == "Incorrect email address or password"

    driver.press_keycode(4)
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="com.ab.apiclient:id/design_menu_item_text" and @text="New Request"]'))).click()

    log_in_user(driver, random_number)  

    delete_user(driver, random_number)

    sleep(5)

    delete_json_file(random_number)

def test_get_user(driver):
    # Gerando dados aleatórios para o usuário
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user(driver, random_number)
    log_in_user(driver, random_number)

    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_token = data['user_token']
    user_id = data['user_id']
    user_name = data['user_name']
    user_email = data['user_email']

    wait = WebDriverWait(driver, 20)

    # Seleciona método HTTP (GET)
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="GET"]'))).click()

    # Insere a URL para obter o perfil
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys("https://practice.expandtesting.com/notes/api/users/profile")

    # Adiciona headers
    add_accept_header(driver)
    
    # Adiciona header de autenticação
    add_token_header(driver, random_number)

    # Envia requisição
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # Visualiza aba "Raw" com resposta
    wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")'))).click()
    wait_for_result_element_and_close_ad(driver)
    response_str = driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/tvResult").text
    response = json.loads(response_str)

    # Validações
    assert response["success"] is True
    assert str(response["status"]) == "200"
    assert response["message"] == "Profile successful"
    assert response["data"]["id"] == user_id
    assert response["data"]["name"] == user_name
    assert response["data"]["email"] == user_email

    # Volta para tela inicial
    driver.press_keycode(4)
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="com.ab.apiclient:id/design_menu_item_text" and @text="New Request"]'))).click()

    delete_user(driver, random_number)

    sleep(5)

    delete_json_file(random_number)

def test_get_user_ur(driver):
    # Gerando dados aleatórios para o usuário
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user(driver, random_number)
    log_in_user(driver, random_number)

    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_token = data['user_token']
    user_id = data['user_id']
    user_name = data['user_name']
    user_email = data['user_email']

    wait = WebDriverWait(driver, 20)

    # Seleciona método HTTP (GET)
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="GET"]'))).click()

    # Insere a URL para obter o perfil
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys("https://practice.expandtesting.com/notes/api/users/profile")

    # Adiciona headers
    add_accept_header(driver)
    
    # Adiciona header de autenticação
    add_token_header_unauthorized(driver, random_number)

    # Envia requisição
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # Visualiza aba "Raw" com resposta
    # wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")'))).click()
    # wait_for_result_element_and_close_ad(driver)
    response_text_element = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/tvResult")
    response_str = response_text_element.text
    response = json.loads(response_str)

    # Validações
    assert response["success"] is False
    assert str(response["status"]) == "401"
    assert response["message"] == "Access token is not valid or has expired, you will need to login"

    # Volta para tela inicial
    driver.press_keycode(4)
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="com.ab.apiclient:id/design_menu_item_text" and @text="New Request"]'))).click()

    delete_user(driver, random_number)

    sleep(5)

    delete_json_file(random_number)

def test_update_user(driver):
    # Gerando dados aleatórios para o usuário
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user(driver, random_number)
    log_in_user(driver, random_number)

    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_token = data['user_token']
    user_id = data['user_id']
    user_name = data['user_name']
    user_email = data['user_email']

    user_phone = Faker().bothify(text='############')
    user_company = Faker().company()[:24]

    wait = WebDriverWait(driver, 20)

    # Seleciona método HTTP (PATCH)
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="PATCH"]'))).click()

    # Insere a URL do endpoint
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys("https://practice.expandtesting.com/notes/api/users/profile")

    # Adiciona headers necessários
    add_accept_header(driver)
    add_content_type_header(driver)
    add_token_header(driver, random_number)

    # Localiza o campo de entrada JSON
    json_input_field = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/etJSONData")

    # Prepara o corpo JSON com os dados das variáveis
    json_body = f'''{{
        "name": "{user_name}",
        "phone": "{user_phone}",
        "company": "{user_company}"
    }}'''

    # Insere o texto formatado no campo
    json_input_field.send_keys(json_body)

    # Envia requisição
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # Visualiza aba "Raw"
    wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")'))).click()
    wait_for_result_element_and_close_ad(driver)
    response_str = driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/tvResult").text
    response = json.loads(response_str)

    # Valida a resposta
    assert response["success"] is True
    assert str(response["status"]) == "200"
    assert response["message"] == "Profile updated successful"
    assert response["data"]["id"] == user_id
    assert response["data"]["name"] == user_name
    assert response["data"]["email"] == user_email
    assert response["data"]["phone"] == user_phone
    assert response["data"]["company"] == user_company

    # Volta à tela inicial
    driver.press_keycode(4)
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="com.ab.apiclient:id/design_menu_item_text" and @text="New Request"]'))).click()

    delete_user(driver, random_number)

    sleep(5)

    delete_json_file(random_number)

def test_update_user_br(driver):
    # Gerando dados aleatórios para o usuário
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user(driver, random_number)
    log_in_user(driver, random_number)

    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_token = data['user_token']
    user_id = data['user_id']
    user_name = data['user_name']
    user_email = data['user_email']

    user_phone = Faker().bothify(text='############')
    user_company = Faker().company()[:24]

    wait = WebDriverWait(driver, 20)

    # Seleciona método HTTP (PATCH)
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="PATCH"]'))).click()

    # Insere a URL do endpoint
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys("https://practice.expandtesting.com/notes/api/users/profile")

    # Adiciona headers necessários
    add_accept_header(driver)
    add_content_type_header(driver)
    add_token_header(driver, random_number)

    # Localiza o campo de entrada JSON
    json_input_field = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/etJSONData")

    # Prepara o corpo JSON com os dados das variáveis
    json_body = f'''{{
        "name": "a@#",
        "phone": "{user_phone}",
        "company": "{user_company}"
    }}'''

    # Insere o texto formatado no campo
    json_input_field.send_keys(json_body)

    # Envia requisição
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # Visualiza aba "Raw"
    # wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")'))).click()
    # wait_for_result_element_and_close_ad(driver)
    response_text_element = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/tvResult")
    response_str = response_text_element.text
    response = json.loads(response_str)

    # Valida a resposta
    assert response["success"] is False
    assert str(response["status"]) == "400"
    assert response["message"] == "User name must be between 4 and 30 characters"

    # Volta à tela inicial
    driver.press_keycode(4)
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="com.ab.apiclient:id/design_menu_item_text" and @text="New Request"]'))).click()

    delete_user(driver, random_number)

    sleep(5)

    delete_json_file(random_number)

def test_update_user_ur(driver):
    # Gerando dados aleatórios para o usuário
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user(driver, random_number)
    log_in_user(driver, random_number)

    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_token = data['user_token']
    user_id = data['user_id']
    user_name = data['user_name']
    user_email = data['user_email']

    user_phone = Faker().bothify(text='############')
    user_company = Faker().company()[:24]

    wait = WebDriverWait(driver, 20)

    # Seleciona método HTTP (PATCH)
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="PATCH"]'))).click()

    # Insere a URL do endpoint
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys("https://practice.expandtesting.com/notes/api/users/profile")

    # Adiciona headers necessários
    add_accept_header(driver)
    add_content_type_header(driver)
    add_token_header_unauthorized(driver, random_number)

    # Localiza o campo de entrada JSON
    json_input_field = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/etJSONData")

    # Prepara o corpo JSON com os dados das variáveis
    json_body = f'''{{
        "name": "{user_name}",
        "phone": "{user_phone}",
        "company": "{user_company}"
    }}'''

    # Insere o texto formatado no campo
    json_input_field.send_keys(json_body)

    # Envia requisição
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # Visualiza aba "Raw"
    # wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")'))).click()
    # wait_for_result_element_and_close_ad(driver)
    response_str = driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/tvResult").text
    response = json.loads(response_str)

    # Valida a resposta
    assert response["success"] is False
    assert str(response["status"]) == "401"
    assert response["message"] == "User name must be between 4 and 30 characters"

    # Volta à tela inicial
    driver.press_keycode(4)
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="com.ab.apiclient:id/design_menu_item_text" and @text="New Request"]'))).click()

    delete_user(driver, random_number)

    sleep(5)

    delete_json_file(random_number)

def test_update_user_password(driver):
    # Gerando dados aleatórios para o usuário
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user(driver, random_number)
    log_in_user(driver, random_number)

    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_token = data['user_token']
    user_password = data['user_password']

    user_updated_password = Faker().password(length=12, special_chars=False, digits=True, upper_case=True, lower_case=True)

    wait = WebDriverWait(driver, 20)

    # Seleciona método HTTP (POST)
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="POST"]'))).click()

    # Insere a URL do endpoint
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys("https://practice.expandtesting.com/notes/api/users/change-password")

    # Adiciona headers necessários
    add_accept_header(driver)
    add_content_type_header(driver)
    add_token_header(driver, random_number)

    # Localiza o campo de entrada JSON
    json_input_field = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/etJSONData")

    # Localiza o campo de entrada JSON
    json_input_field = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/etJSONData")

    # Prepara o corpo JSON com os dados das variáveis
    json_body = f'''{{
        "currentPassword": "{user_password}",
        "newPassword": "{user_updated_password}"
    }}'''

    # Insere o texto formatado no campo
    json_input_field.send_keys(json_body)

    # Envia requisição
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # Visualiza aba "Raw"
    wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")'))).click()
    wait_for_result_element_and_close_ad(driver)
    response_str = driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/tvResult").text
    response = json.loads(response_str)

    # Valida a resposta
    assert response["success"] is True
    assert str(response["status"]) == "200"
    assert response["message"] == "The password was successfully updated"

    # Atualiza o JSON com a nova senha
    data["user_password"] = user_updated_password
    with open(filepath, 'w') as file:
        json.dump(data, file)

    # Volta à tela inicial
    driver.press_keycode(4)
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="com.ab.apiclient:id/design_menu_item_text" and @text="New Request"]'))).click()

    # Cleanup
    delete_user(driver, random_number)

    sleep(5)

    delete_json_file(random_number)

def test_update_user_password_br(driver):
    # Gerando dados aleatórios para o usuário
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user(driver, random_number)
    log_in_user(driver, random_number)

    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_token = data['user_token']
    user_password = data['user_password']

    user_updated_password = Faker().password(length=12, special_chars=False, digits=True, upper_case=True, lower_case=True)

    wait = WebDriverWait(driver, 20)

    # Seleciona método HTTP (POST)
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="POST"]'))).click()

    # Insere a URL do endpoint
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys("https://practice.expandtesting.com/notes/api/users/change-password")

    # Adiciona headers necessários
    add_accept_header(driver)
    add_content_type_header(driver)
    add_token_header(driver, random_number)

    # Localiza o campo de entrada JSON
    json_input_field = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/etJSONData")

    # Localiza o campo de entrada JSON
    json_input_field = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/etJSONData")

    # Prepara o corpo JSON com os dados das variáveis
    json_body = f'''{{
        "currentPassword": "{user_password}",
        "newPassword": "123"
    }}'''

    # Insere o texto formatado no campo
    json_input_field.send_keys(json_body)

    # Envia requisição
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # Visualiza aba "Raw"
    # wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")'))).click()
    # wait_for_result_element_and_close_ad(driver)
    response_text_element = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/tvResult")
    response_str = response_text_element.text
    response = json.loads(response_str)

    # Valida a resposta
    assert response["success"] is False
    assert str(response["status"]) == "400"
    assert response["message"] == "New password must be between 6 and 30 characters"

    # Volta à tela inicial
    driver.press_keycode(4)
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="com.ab.apiclient:id/design_menu_item_text" and @text="New Request"]'))).click()

    # Cleanup
    delete_user(driver, random_number)

    sleep(5)

    delete_json_file(random_number)

def test_update_user_password_ur(driver):
    # Gerando dados aleatórios para o usuário
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user(driver, random_number)
    log_in_user(driver, random_number)

    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_token = data['user_token']
    user_password = data['user_password']

    user_updated_password = Faker().password(length=12, special_chars=False, digits=True, upper_case=True, lower_case=True)

    wait = WebDriverWait(driver, 20)

    # Seleciona método HTTP (POST)
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="POST"]'))).click()

    # Insere a URL do endpoint
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys("https://practice.expandtesting.com/notes/api/users/change-password")

    # Adiciona headers necessários
    add_accept_header(driver)
    add_content_type_header(driver)
    add_token_header_unauthorized(driver, random_number)

    # Localiza o campo de entrada JSON
    json_input_field = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/etJSONData")

    # Localiza o campo de entrada JSON
    json_input_field = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/etJSONData")

    # Prepara o corpo JSON com os dados das variáveis
    json_body = f'''{{
        "currentPassword": "{user_password}",
        "newPassword": "{user_updated_password}"
    }}'''

    # Insere o texto formatado no campo
    json_input_field.send_keys(json_body)

    # Envia requisição
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # Visualiza aba "Raw"
    # wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")'))).click()
    # wait_for_result_element_and_close_ad(driver)
    response_text_element = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/tvResult")
    response_str = response_text_element.text
    response = json.loads(response_str)

    # Valida a resposta
    assert response["success"] is False
    assert str(response["status"]) == "401"
    assert response["message"] == "Access token is not valid or has expired, you will need to login"

    # Volta à tela inicial
    driver.press_keycode(4)
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="com.ab.apiclient:id/design_menu_item_text" and @text="New Request"]'))).click()

    # Cleanup
    delete_user(driver, random_number)

    sleep(5)

    delete_json_file(random_number)

def test_logout_user(driver):
    # Gerando dados aleatórios para o usuário
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user(driver, random_number)
    log_in_user(driver, random_number)

    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_token = data['user_token']

    wait = WebDriverWait(driver, 20)

    # Seleciona método HTTP (DELETE)
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="DELETE"]'))).click()

    # Insere a URL do endpoint
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys("https://practice.expandtesting.com/notes/api/users/logout")

    # Adiciona headers necessários
    add_accept_header(driver)
    add_token_header(driver, random_number)

    # Limpa o campo de body se houver algo
    json_input_field = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/etJSONData")
    json_input_field.clear()

    # Envia requisição
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # Visualiza aba "Raw"
    wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")'))).click()
    wait_for_result_element_and_close_ad(driver)
    response_str = driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/tvResult").text
    response = json.loads(response_str)

    # Valida a resposta
    assert response["success"] is True
    assert str(response["status"]) == "200"
    assert response["message"] == "User has been successfully logged out"

    # Volta à tela inicial
    driver.press_keycode(4)
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="com.ab.apiclient:id/design_menu_item_text" and @text="New Request"]'))).click()

    # Cleanup

    #login again to grab a new token to be used in the delete method
    log_in_user(driver, random_number)

    delete_user(driver, random_number)

    sleep(5)

    delete_json_file(random_number)

def test_logout_user_ur(driver):
    # Gerando dados aleatórios para o usuário
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user(driver, random_number)
    log_in_user(driver, random_number)

    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_token = data['user_token']

    wait = WebDriverWait(driver, 20)

    # Seleciona método HTTP (DELETE)
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="DELETE"]'))).click()

    # Insere a URL do endpoint
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys("https://practice.expandtesting.com/notes/api/users/logout")

    # Adiciona headers necessários
    add_accept_header(driver)
    add_token_header_unauthorized(driver, random_number)

    # Limpa o campo de body se houver algo
    json_input_field = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/etJSONData")
    json_input_field.clear()

    # Envia requisição
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # Visualiza aba "Raw"
    # wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")'))).click()
    # wait_for_result_element_and_close_ad(driver)
    response_text_element = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/tvResult")
    response_str = response_text_element.text
    response = json.loads(response_str)

    # Valida a resposta
    assert response["success"] is False
    assert str(response["status"]) == "401"
    assert response["message"] == "Access token is not valid or has expired, you will need to login"

    # Volta à tela inicial
    driver.press_keycode(4)
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="com.ab.apiclient:id/design_menu_item_text" and @text="New Request"]'))).click()

    delete_user(driver, random_number)

    sleep(5)

    delete_json_file(random_number)

def test_delete_user(driver):
    # Gerando dados aleatórios para o usuário
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user(driver, random_number)
    log_in_user(driver, random_number)

    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_token = data['user_token']
    wait = WebDriverWait(driver, 20)

    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="DELETE"]'))).click()

    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys("https://practice.expandtesting.com/notes/api/users/delete-account")

    add_accept_header(driver)
    add_token_header(driver, random_number)

    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")'))).click()
    wait_for_result_element_and_close_ad(driver)
    response_str = driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/tvResult").text
    response = json.loads(response_str)

    assert response["success"] is True
    assert str(response["status"]) == "200"
    assert response["message"] == "Account successfully deleted"

    driver.press_keycode(4)
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="com.ab.apiclient:id/design_menu_item_text" and @text="New Request"]'))).click()

    sleep(5)

    delete_json_file(random_number)

def test_delete_user_ur(driver):
    # Gerando dados aleatórios para o usuário
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user(driver, random_number)
    log_in_user(driver, random_number)

    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_token = data['user_token']
    wait = WebDriverWait(driver, 20)

    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="DELETE"]'))).click()

    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys("https://practice.expandtesting.com/notes/api/users/delete-account")

    add_accept_header(driver)
    add_token_header_unauthorized(driver, random_number)

    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")'))).click()
    # wait_for_result_element_and_close_ad(driver)
    response_text_element = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/tvResult")
    response_str = response_text_element.text
    response = json.loads(response_str)

    # Valida a resposta
    assert response["success"] is False
    assert str(response["status"]) == "401"
    assert response["message"] == "Access token is not valid or has expired, you will need to login"

    driver.press_keycode(4)
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="com.ab.apiclient:id/design_menu_item_text" and @text="New Request"]'))).click()

    sleep(5)

    delete_user(random_number)

    delete_json_file(random_number)
