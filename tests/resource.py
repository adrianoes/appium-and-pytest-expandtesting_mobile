from subprocess import run
from time import sleep
from appium.webdriver.webdriver import WebDriver
from faker import Faker
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
import os
import json

TIMEOUT = 20

def wait_until_element_visible(driver, by, value, timeout=TIMEOUT):
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by, value)))

def wait_for_result_element_and_close_ad(driver):
    try:
        wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/tvResult", timeout=20)
    except TimeoutException:
        close_full_screen_ad(driver)
        wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/tvResult", timeout=10)

def add_accept_header(driver):
    wait_until_element_visible(driver, AppiumBy.CLASS_NAME, "android.widget.ImageView").click()
    wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/iconDown").click()
    wait_until_element_visible(driver, AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Accept")').click()
    wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/iconDownVal").click()
    wait_until_element_visible(driver, AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("application/xml")').click()

def add_content_type_header(driver):
    wait_until_element_visible(driver, AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.ImageView").instance(0)').click()
    wait_until_element_visible(driver, AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.ab.apiclient:id/iconDown").instance(1)').click()
    wait_until_element_visible(driver, AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Content-Type")').click()
    wait_until_element_visible(driver, AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.ab.apiclient:id/iconDownVal").instance(1)').click()
    wait_until_element_visible(driver, AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("application/json")').click()

def log_in_user(driver, random_number):
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

def delete_user(driver, random_number):
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

def increasing_request_response_timeout(driver):
    wait_until_element_visible(driver, AppiumBy.CLASS_NAME, "android.widget.ImageButton").click()
    wait_until_element_visible(driver, AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Settings")').click()

    wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/etTimeoutConnection").clear()
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/etTimeoutConnection").send_keys("120")

    wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/etTimeoutREAD").clear()
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/etTimeoutREAD").send_keys("120")

    wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/etTimeoutWRITE").clear()
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/etTimeoutWRITE").send_keys("120")

    wait_until_element_visible(driver, AppiumBy.CLASS_NAME, "android.widget.ImageButton").click()
    wait_until_element_visible(driver, AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("New Request")').click()

def close_full_screen_ad(driver: WebDriver):
    # Implementar aqui conforme o comportamento do ad
    pass

def add_token_header(driver, random_number):
    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_token = data['user_token']

    wait = WebDriverWait(driver, 20)

    # Abrir painel de header
    wait.until(EC.visibility_of_element_located((
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.widget.ImageView").instance(0)'
    ))).click()

    # Preencher header com chave e token
    wait.until(EC.visibility_of_element_located((
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("Key")'
    ))).send_keys("x-auth-token")

    wait.until(EC.visibility_of_element_located((
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("Value")'
    ))).send_keys(user_token)

def add_token_header_unauthorized(driver, random_number):
    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_token = data['user_token']
    invalid_token = f"@{user_token}"

    wait = WebDriverWait(driver, 20)

    # Abrir painel de header
    wait.until(EC.visibility_of_element_located((
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.widget.ImageView").instance(0)'
    ))).click()

    # Preencher header com chave e token inválido
    wait.until(EC.visibility_of_element_located((
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("Key")'
    ))).send_keys("x-auth-token")

    wait.until(EC.visibility_of_element_located((
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("Value")'
    ))).send_keys(invalid_token)

def delete_json_file(random_number):
    filepath = f"tests/fixtures/testdata-{random_number}.json"
    if os.path.exists(filepath):
        os.remove(filepath)
        print("Json file deleted")
    else:
        print("Json file not found")

def create_user(driver, random_number):
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









