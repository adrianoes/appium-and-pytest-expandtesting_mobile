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
    create_note,
    create_2nd_note,
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

def test_create_note(driver):
    # Gerando dados aleatórios para o usuário
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user(driver, random_number)
    log_in_user(driver, random_number)

    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_token = data['user_token']
    user_id = data['user_id']

    note_title = Faker().sentence(4)
    note_description = Faker().sentence(5)
    note_category = Faker().random_element(elements=('Home', 'Personal', 'Work'))

    wait = WebDriverWait(driver, 20)

    # Seleciona método HTTP (POST)
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="POST"]'))).click()

    # Insere a URL do endpoint
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys("https://practice.expandtesting.com/notes/api/notes")

    # Adiciona headers necessários
    add_accept_header(driver)
    add_content_type_header(driver)
    add_token_header(driver, random_number)

    # Localiza o campo de entrada JSON
    json_input_field = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/etJSONData")

    # Prepara o corpo JSON com os dados da nota
    json_body = f'''{{
        "title": "{note_title}",
        "description": "{note_description}",
        "category": "{note_category}"
    }}'''

    # Insere o corpo JSON no campo apropriado
    json_input_field.clear()
    json_input_field.send_keys(json_body)

    # Envia requisição
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # Visualiza aba "Raw"
    wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")'))).click()
    wait_for_result_element_and_close_ad(driver)
    response_str = driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/tvResult").text
    response = json.loads(response_str)

    # Valida a resposta principal
    assert response["success"] is True
    assert str(response["status"]) == "200"
    assert response["message"] == "Note successfully created"

    note_data = response["data"]

    # Valida que os dados retornados correspondem ao esperado
    assert note_data["user_id"] == user_id
    assert note_data["title"] == note_title
    assert note_data["description"] == note_description
    assert note_data["category"] == note_category
    assert note_data["completed"] is False

    # Atualiza o JSON com os dados da nota
    data.update({
        "note_id": note_data["id"],
        "note_title": note_data["title"],
        "note_description": note_data["description"],
        "note_category": note_data["category"],
        "note_completed": note_data["completed"],
        "note_created_at": note_data["created_at"],
        "note_updated_at": note_data["updated_at"]
    })

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

def test_create_note_br(driver):
    # Gerando dados aleatórios para o usuário
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user(driver, random_number)
    log_in_user(driver, random_number)

    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_token = data['user_token']
    user_id = data['user_id']

    note_title = Faker().sentence(4)
    note_description = Faker().sentence(5)
    note_category = Faker().random_element(elements=('Home', 'Personal', 'Work'))

    wait = WebDriverWait(driver, 20)

    # Seleciona método HTTP (POST)
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="POST"]'))).click()

    # Insere a URL do endpoint
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys("https://practice.expandtesting.com/notes/api/notes")

    # Adiciona headers necessários
    add_accept_header(driver)
    add_content_type_header(driver)
    add_token_header(driver, random_number)

    # Localiza o campo de entrada JSON
    json_input_field = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/etJSONData")

    # Prepara o corpo JSON com os dados da nota
    json_body = f'''{{
        "title": "{note_title}",
        "description": "{note_description}",
        "category": "a"
    }}'''

    # Insere o corpo JSON no campo apropriado
    json_input_field.clear()
    json_input_field.send_keys(json_body)

    # Envia requisição
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # Visualiza aba "Raw"
    # wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")'))).click()
    # wait_for_result_element_and_close_ad(driver)
    response_text_element = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/tvResult")
    response_str = response_text_element.text
    response = json.loads(response_str)

    # Valida a resposta principal
    assert response["success"] is False
    assert str(response["status"]) == "400"
    assert response["message"] == "Category must be one of the categories: Home, Work, Personal"

    # Volta à tela inicial
    driver.press_keycode(4)
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="com.ab.apiclient:id/design_menu_item_text" and @text="New Request"]'))).click()

    # Cleanup
    delete_user(driver, random_number)

    sleep(5)

    delete_json_file(random_number)

def test_create_note_ur(driver):
    # Gerando dados aleatórios para o usuário
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user(driver, random_number)
    log_in_user(driver, random_number)

    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_token = data['user_token']
    user_id = data['user_id']

    note_title = Faker().sentence(4)
    note_description = Faker().sentence(5)
    note_category = Faker().random_element(elements=('Home', 'Personal', 'Work'))

    wait = WebDriverWait(driver, 20)

    # Seleciona método HTTP (POST)
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="POST"]'))).click()

    # Insere a URL do endpoint
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys("https://practice.expandtesting.com/notes/api/notes")

    # Adiciona headers necessários
    add_accept_header(driver)
    add_content_type_header(driver)
    add_token_header_unauthorized(driver, random_number)

    # Localiza o campo de entrada JSON
    json_input_field = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/etJSONData")

    # Prepara o corpo JSON com os dados da nota
    json_body = f'''{{
        "title": "{note_title}",
        "description": "{note_description}",
        "category": "{note_category}"
    }}'''

    # Insere o corpo JSON no campo apropriado
    json_input_field.clear()
    json_input_field.send_keys(json_body)

    # Envia requisição
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # Visualiza aba "Raw"
    # wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")'))).click()
    # wait_for_result_element_and_close_ad(driver)
    response_text_element = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/tvResult")
    response_str = response_text_element.text
    response = json.loads(response_str)

    # Valida a resposta principal
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

def test_get_notes(driver):
    # Gerando dados aleatórios para o usuário
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user(driver, random_number)
    log_in_user(driver, random_number)
    create_note(driver, random_number)
    create_2nd_note(driver, random_number) 
    
    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    wait = WebDriverWait(driver, 20)

    # Seleciona método HTTP (GET)
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="GET"]'))).click()

    # Insere a URL para obter todas as notas
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys("https://practice.expandtesting.com/notes/api/notes")

    # Adiciona headers
    add_accept_header(driver)
    add_token_header(driver, random_number)

    # Envia requisição
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # Visualiza aba "Raw"
    wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")'))).click()
    wait_for_result_element_and_close_ad(driver)
    response_str = driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/tvResult").text
    response = json.loads(response_str)

    # Validação da resposta principal
    assert response["success"] is True
    assert str(response["status"]) == "200"
    assert response["message"] == "Notes successfully retrieved"

    notes = response["data"]
    assert len(notes) == 2  # Deve retornar duas notas

    # Lê os dados esperados do arquivo JSON
    user_id = data["user_id"]

    # --- Nota 2 (a mais recente, index 0) ---
    note_2 = notes[0]
    assert note_2["id"] == data["note_id_2"]
    assert note_2["user_id"] == user_id
    assert note_2["title"] == data["note_title_2"]
    assert note_2["description"] == data["note_description_2"]
    assert note_2["category"] == data["note_category_2"]
    assert note_2["completed"] == data["note_completed_2"]
    assert note_2["created_at"] == data["note_created_at_2"]
    assert note_2["updated_at"] == data["note_updated_at_2"]

    # --- Nota 1 (a primeira criada, index 1) ---
    note_1 = notes[1]
    assert note_1["id"] == data["note_id"]
    assert note_1["user_id"] == user_id
    assert note_1["title"] == data["note_title"]
    assert note_1["description"] == data["note_description"]
    assert note_1["category"] == data["note_category"]
    assert note_1["completed"] == data["note_completed"]
    assert note_1["created_at"] == data["note_created_at"]
    assert note_1["updated_at"] == data["note_updated_at"]

    # Volta à tela inicial
    driver.press_keycode(4)
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="com.ab.apiclient:id/design_menu_item_text" and @text="New Request"]'))).click()

    # Cleanup
    delete_user(driver, random_number)

    sleep(5)

    delete_json_file(random_number)

def test_get_notes_ur(driver):
    # Gerando dados aleatórios para o usuário
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user(driver, random_number)
    log_in_user(driver, random_number)
    create_note(driver, random_number)
    create_2nd_note(driver, random_number) 
    
    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    wait = WebDriverWait(driver, 20)

    # Seleciona método HTTP (GET)
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="GET"]'))).click()

    # Insere a URL para obter todas as notas
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys("https://practice.expandtesting.com/notes/api/notes")

    # Adiciona headers
    add_accept_header(driver)
    add_token_header_unauthorized(driver, random_number)

    # Envia requisição
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # Visualiza aba "Raw"
    # wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")'))).click()
    # wait_for_result_element_and_close_ad(driver)
    response_text_element = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/tvResult")
    response_str = response_text_element.text
    response = json.loads(response_str)

    # Validação da resposta principal
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

def test_get_note(driver):
    # Gerando dados aleatórios para o usuário
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user(driver, random_number)
    log_in_user(driver, random_number)
    create_note(driver, random_number)

    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_token = data['user_token']
    user_id = data['user_id']

    # Dados da nota armazenados no JSON após a criação
    note_id = data['note_id']
    note_title = data['note_title']
    note_description = data['note_description']
    note_category = data['note_category']
    note_completed = data['note_completed']
    note_created_at = data['note_created_at']
    note_updated_at = data['note_updated_at']

    wait = WebDriverWait(driver, 20)

    # Seleciona método HTTP (GET)
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="GET"]'))).click()

    # Insere a URL com o ID da nota
    get_note_url = f"https://practice.expandtesting.com/notes/api/notes/{note_id}"
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys(get_note_url)

    # Adiciona headers obrigatórios
    add_accept_header(driver)
    add_token_header(driver, random_number)

    # Envia requisição
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # Visualiza aba "Raw"
    wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")'))).click()
    wait_for_result_element_and_close_ad(driver)
    response_str = driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/tvResult").text
    response = json.loads(response_str)

    # Valida resposta principal
    assert response["success"] is True
    assert str(response["status"]) == "200"
    assert response["message"] == "Note successfully retrieved"

    # Valida dados retornados
    note_data = response["data"]
    assert note_data["id"] == note_id
    assert note_data["user_id"] == user_id
    assert note_data["title"] == note_title
    assert note_data["description"] == note_description
    assert note_data["category"] == note_category
    assert note_data["completed"] == note_completed
    assert note_data["created_at"] == note_created_at
    assert note_data["updated_at"] == note_updated_at

    # Volta à tela inicial
    driver.press_keycode(4)
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="com.ab.apiclient:id/design_menu_item_text" and @text="New Request"]'))).click()

    # Cleanup
    delete_user(driver, random_number)

    sleep(5)

    delete_json_file(random_number)

def test_get_note_ur(driver):
    # Gerando dados aleatórios para o usuário
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user(driver, random_number)
    log_in_user(driver, random_number)
    create_note(driver, random_number)

    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_token = data['user_token']
    user_id = data['user_id']

    # Dados da nota armazenados no JSON após a criação
    note_id = data['note_id']
    note_title = data['note_title']
    note_description = data['note_description']
    note_category = data['note_category']
    note_completed = data['note_completed']
    note_created_at = data['note_created_at']
    note_updated_at = data['note_updated_at']

    wait = WebDriverWait(driver, 20)

    # Seleciona método HTTP (GET)
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="GET"]'))).click()

    # Insere a URL com o ID da nota
    get_note_url = f"https://practice.expandtesting.com/notes/api/notes/{note_id}"
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys(get_note_url)

    # Adiciona headers obrigatórios
    add_accept_header(driver)
    add_token_header_unauthorized(driver, random_number)

    # Envia requisição
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # Visualiza aba "Raw"
    # wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")'))).click()
    # wait_for_result_element_and_close_ad(driver)
    response_text_element = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/tvResult")
    response_str = response_text_element.text
    response = json.loads(response_str)

    # Validação da resposta principal
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

def test_update_note(driver):
    # Gerando dados aleatórios para o usuário
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user(driver, random_number)
    log_in_user(driver, random_number)
    create_note(driver, random_number)

    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_token = data['user_token']
    user_id = data['user_id']

    # Dados atuais da nota
    note_id = data['note_id']
    note_created_at = data['note_created_at']

    # Gera valores atualizados com Faker
    note_updated_title = Faker().sentence(4)
    note_updated_description = Faker().sentence(5)
    note_updated_category = Faker().random_element(elements=('Home', 'Personal', 'Work'))
    note_updated_completed = True

    wait = WebDriverWait(driver, 20)

    # Seleciona método HTTP (PUT)
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="PUT"]'))).click()

    # Insere a URL com o ID da nota
    update_note_url = f"https://practice.expandtesting.com/notes/api/notes/{note_id}"
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys(update_note_url)

    # Adiciona headers obrigatórios
    add_accept_header(driver)
    add_content_type_header(driver)  # application/x-www-form-urlencoded
    add_token_header(driver, random_number)

    # Prepara o corpo em formato x-www-form-urlencoded
    form_body = f"title={note_updated_title}&description={note_updated_description}&completed={str(note_updated_completed).lower()}&category={note_updated_category}"

    # Localiza o campo de entrada JSON
    json_input_field = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/etJSONData")

    # Prepara o corpo JSON com os dados da nota
    json_body = f'''{{
        "title": "{note_updated_title}",
        "description": "{note_updated_description}",
        "category": "{note_updated_category}",
        "completed": "{str(note_updated_completed).lower()}"
    }}'''

    # Insere o corpo JSON no campo apropriado
    json_input_field.clear()
    json_input_field.send_keys(json_body)

    # Envia requisição
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # Visualiza aba "Raw"
    wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")'))).click()
    wait_for_result_element_and_close_ad(driver)
    response_str = driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/tvResult").text
    response = json.loads(response_str)

    # Valida resposta principal
    assert response["success"] is True
    assert str(response["status"]) == "200"
    assert response["message"] == "Note successfully Updated"

    note_data = response["data"]

    # Valida os dados atualizados
    assert note_data["id"] == note_id
    assert note_data["user_id"] == user_id
    assert note_data["title"] == note_updated_title
    assert note_data["description"] == note_updated_description
    assert note_data["category"] == note_updated_category
    assert note_data["completed"] is True
    assert note_data["created_at"] == note_created_at
    assert note_data["updated_at"] != note_created_at  # updated_at deve ser diferente após update

    # Atualiza JSON local com os novos dados
    data.update({
        "note_title": note_data["title"],
        "note_description": note_data["description"],
        "note_category": note_data["category"],
        "note_completed": note_data["completed"],
        "note_updated_at": note_data["updated_at"]
    })

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

def test_update_note_br(driver):
    # Gerando dados aleatórios para o usuário
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user(driver, random_number)
    log_in_user(driver, random_number)
    create_note(driver, random_number)

    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_token = data['user_token']
    user_id = data['user_id']

    # Dados atuais da nota
    note_id = data['note_id']
    note_created_at = data['note_created_at']

    # Gera valores atualizados com Faker
    note_updated_title = Faker().sentence(4)
    note_updated_description = Faker().sentence(5)
    note_updated_category = Faker().random_element(elements=('Home', 'Personal', 'Work'))
    note_updated_completed = True

    wait = WebDriverWait(driver, 20)

    # Seleciona método HTTP (PUT)
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="PUT"]'))).click()

    # Insere a URL com o ID da nota
    update_note_url = f"https://practice.expandtesting.com/notes/api/notes/{note_id}"
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys(update_note_url)

    # Adiciona headers obrigatórios
    add_accept_header(driver)
    add_content_type_header(driver)  # application/x-www-form-urlencoded
    add_token_header(driver, random_number)

    # Prepara o corpo em formato x-www-form-urlencoded
    form_body = f"title={note_updated_title}&description={note_updated_description}&completed={str(note_updated_completed).lower()}&category={note_updated_category}"

    # Localiza o campo de entrada JSON
    json_input_field = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/etJSONData")

    # Prepara o corpo JSON com os dados da nota
    json_body = f'''{{
        "title": "{note_updated_title}",
        "description": "{note_updated_description}",
        "category": "a",
        "completed": "{str(note_updated_completed).lower()}"
    }}'''

    # Insere o corpo JSON no campo apropriado
    json_input_field.clear()
    json_input_field.send_keys(json_body)

    # Envia requisição
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # Visualiza aba "Raw"
    # wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")'))).click()
    # wait_for_result_element_and_close_ad(driver)
    response_text_element = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/tvResult")
    response_str = response_text_element.text
    response = json.loads(response_str)

    # Valida resposta principal
    assert response["success"] is False
    assert str(response["status"]) == "400"
    assert response["message"] == "Category must be one of the categories: Home, Work, Personal"

    # Volta à tela inicial
    driver.press_keycode(4)
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="com.ab.apiclient:id/design_menu_item_text" and @text="New Request"]'))).click()

    # Cleanup
    delete_user(driver, random_number)

    sleep(5)

    delete_json_file(random_number)

def test_update_note_ur(driver):
    # Gerando dados aleatórios para o usuário
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user(driver, random_number)
    log_in_user(driver, random_number)
    create_note(driver, random_number)

    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_token = data['user_token']
    user_id = data['user_id']

    # Dados atuais da nota
    note_id = data['note_id']
    note_created_at = data['note_created_at']

    # Gera valores atualizados com Faker
    note_updated_title = Faker().sentence(4)
    note_updated_description = Faker().sentence(5)
    note_updated_category = Faker().random_element(elements=('Home', 'Personal', 'Work'))
    note_updated_completed = True

    wait = WebDriverWait(driver, 20)

    # Seleciona método HTTP (PUT)
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="PUT"]'))).click()

    # Insere a URL com o ID da nota
    update_note_url = f"https://practice.expandtesting.com/notes/api/notes/{note_id}"
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys(update_note_url)

    # Adiciona headers obrigatórios
    add_accept_header(driver)
    add_content_type_header(driver)  # application/x-www-form-urlencoded
    add_token_header_unauthorized(driver, random_number)

    # Prepara o corpo em formato x-www-form-urlencoded
    form_body = f"title={note_updated_title}&description={note_updated_description}&completed={str(note_updated_completed).lower()}&category={note_updated_category}"

    # Localiza o campo de entrada JSON
    json_input_field = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/etJSONData")

    # Prepara o corpo JSON com os dados da nota
    json_body = f'''{{
        "title": "{note_updated_title}",
        "description": "{note_updated_description}",
        "category": "{note_updated_category}",
        "completed": "{str(note_updated_completed).lower()}"
    }}'''

    # Insere o corpo JSON no campo apropriado
    json_input_field.clear()
    json_input_field.send_keys(json_body)

    # Envia requisição
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # Visualiza aba "Raw"
    # wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")'))).click()
    # wait_for_result_element_and_close_ad(driver)
    response_text_element = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/tvResult")
    response_str = response_text_element.text
    response = json.loads(response_str)

    # Valida resposta principal
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

def test_update_note_status(driver):
    # Gerando dados aleatórios para o usuário
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user(driver, random_number)
    log_in_user(driver, random_number)
    create_note(driver, random_number)

    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_token = data['user_token']
    user_id = data['user_id']

    # Dados da nota armazenados no JSON após a criação
    note_id = data['note_id']
    note_title = data['note_title']
    note_description = data['note_description']
    note_category = data['note_category']
    note_created_at = data['note_created_at']
    note_updated_at = data['note_updated_at']

    note_updated_completed = True

    wait = WebDriverWait(driver, 20)

    # Seleciona método HTTP (PUT)
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="PATCH"]'))).click()

    # Insere a URL com o ID da nota
    update_note_url = f"https://practice.expandtesting.com/notes/api/notes/{note_id}"
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys(update_note_url)

    # Adiciona headers obrigatórios
    add_accept_header(driver)
    add_content_type_header(driver)  # application/x-www-form-urlencoded
    add_token_header(driver, random_number)

    # Localiza o campo de entrada JSON
    json_input_field = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/etJSONData")

    # Prepara o corpo JSON com os dados da nota
    json_body = f'''{{
        "completed": "{str(note_updated_completed).lower()}"
    }}'''

    # Insere o corpo JSON no campo apropriado
    json_input_field.clear()
    json_input_field.send_keys(json_body)

    # Envia requisição
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # Visualiza aba "Raw"
    wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")'))).click()
    wait_for_result_element_and_close_ad(driver)
    response_str = driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/tvResult").text
    response = json.loads(response_str)

    # Valida resposta principal
    assert response["success"] is True
    assert str(response["status"]) == "200"
    assert response["message"] == "Note successfully Updated"

    note_data = response["data"]

    # Valida os dados atualizados
    assert note_data["id"] == note_id
    assert note_data["user_id"] == user_id
    assert note_data["title"] == note_title
    assert note_data["description"] == note_description
    assert note_data["category"] == note_category
    assert note_data["completed"] is True
    assert note_data["created_at"] == note_created_at
    assert note_data["updated_at"] != note_updated_at  # updated_at deve ser diferente após update

    # Atualiza JSON local com os novos dados
    data.update({
        "note_completed": note_data["completed"]
    })

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

def test_update_note_status_br(driver):
    # Gerando dados aleatórios para o usuário
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user(driver, random_number)
    log_in_user(driver, random_number)
    create_note(driver, random_number)

    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_token = data['user_token']
    user_id = data['user_id']

    # Dados da nota armazenados no JSON após a criação
    note_id = data['note_id']
    note_title = data['note_title']
    note_description = data['note_description']
    note_category = data['note_category']
    note_created_at = data['note_created_at']
    note_updated_at = data['note_updated_at']

    note_updated_completed = True

    wait = WebDriverWait(driver, 20)

    # Seleciona método HTTP (PUT)
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="PATCH"]'))).click()

    # Insere a URL com o ID da nota
    update_note_url = f"https://practice.expandtesting.com/notes/api/notes/{note_id}"
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys(update_note_url)

    # Adiciona headers obrigatórios
    add_accept_header(driver)
    add_content_type_header(driver)  # application/x-www-form-urlencoded
    add_token_header(driver, random_number)

    # Localiza o campo de entrada JSON
    json_input_field = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/etJSONData")

    # Prepara o corpo JSON com os dados da nota
    json_body = f'''{{
        "completed": "a"
    }}'''

    # Insere o corpo JSON no campo apropriado
    json_input_field.clear()
    json_input_field.send_keys(json_body)

    # Envia requisição
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # Visualiza aba "Raw"
    # wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")'))).click()
    # wait_for_result_element_and_close_ad(driver)
    response_text_element = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/tvResult")
    response_str = response_text_element.text
    response = json.loads(response_str)

    # Valida resposta principal
    assert response["success"] is False
    assert str(response["status"]) == "400"
    assert response["message"] == "Note completed status must be boolean"

    # Volta à tela inicial
    driver.press_keycode(4)
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="com.ab.apiclient:id/design_menu_item_text" and @text="New Request"]'))).click()

    # Cleanup
    delete_user(driver, random_number)

    sleep(5)

    delete_json_file(random_number)

def test_update_note_status_ur(driver):
    # Gerando dados aleatórios para o usuário
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user(driver, random_number)
    log_in_user(driver, random_number)
    create_note(driver, random_number)

    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_token = data['user_token']
    user_id = data['user_id']

    # Dados da nota armazenados no JSON após a criação
    note_id = data['note_id']
    note_title = data['note_title']
    note_description = data['note_description']
    note_category = data['note_category']
    note_created_at = data['note_created_at']
    note_updated_at = data['note_updated_at']

    note_updated_completed = True

    wait = WebDriverWait(driver, 20)

    # Seleciona método HTTP (PUT)
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="PATCH"]'))).click()

    # Insere a URL com o ID da nota
    update_note_url = f"https://practice.expandtesting.com/notes/api/notes/{note_id}"
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys(update_note_url)

    # Adiciona headers obrigatórios
    add_accept_header(driver)
    add_content_type_header(driver)  # application/x-www-form-urlencoded
    add_token_header_unauthorized(driver, random_number)

    # Localiza o campo de entrada JSON
    json_input_field = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/etJSONData")

    # Prepara o corpo JSON com os dados da nota
    json_body = f'''{{
        "completed": "{note_updated_completed}"
    }}'''

    # Insere o corpo JSON no campo apropriado
    json_input_field.clear()
    json_input_field.send_keys(json_body)

    # Envia requisição
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # Visualiza aba "Raw"
    # wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")'))).click()
    # wait_for_result_element_and_close_ad(driver)
    response_text_element = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/tvResult")
    response_str = response_text_element.text
    response = json.loads(response_str)

    # Valida resposta principal
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

def test_delete_note(driver):
    # Gerando dados aleatórios para o usuário
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user(driver, random_number)
    log_in_user(driver, random_number)
    create_note(driver, random_number)

    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_token = data['user_token']

    # Dados da nota armazenados no JSON após a criação
    note_id = data['note_id']

    wait = WebDriverWait(driver, 20)

    # Seleciona método HTTP (DELETE)
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="DELETE"]'))).click()

    # Insere a URL com o ID da nota
    delete_note_url = f"https://practice.expandtesting.com/notes/api/notes/{note_id}"
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys(delete_note_url)

    # Adiciona headers obrigatórios
    add_accept_header(driver)
    add_token_header(driver, random_number)

    # Envia requisição
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # Visualiza aba "Raw"
    wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")'))).click()
    wait_for_result_element_and_close_ad(driver)
    response_str = driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/tvResult").text
    response = json.loads(response_str)

    # Valida resposta principal
    assert response["success"] is True
    assert str(response["status"]) == "200"
    assert response["message"] == "Note successfully deleted"

    # Remove dados da nota do JSON local
    for key in list(data.keys()):
        if key.startswith("note_"):
            del data[key]

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

def test_delete_note_br(driver):
    # Gerando dados aleatórios para o usuário
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user(driver, random_number)
    log_in_user(driver, random_number)
    create_note(driver, random_number)

    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_token = data['user_token']

    # Dados da nota armazenados no JSON após a criação
    note_id = data['note_id']

    wait = WebDriverWait(driver, 20)

    # Seleciona método HTTP (DELETE)
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="DELETE"]'))).click()

    # Insere a URL com o ID da nota
    delete_note_url = f"https://practice.expandtesting.com/notes/api/notes/@{note_id}"
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys(delete_note_url)

    # Adiciona headers obrigatórios
    add_accept_header(driver)
    add_token_header(driver, random_number)

    # Envia requisição
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # Visualiza aba "Raw"
    # wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")'))).click()
    # wait_for_result_element_and_close_ad(driver)
    response_text_element = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/tvResult")
    response_str = response_text_element.text
    response = json.loads(response_str)

    # Valida resposta principal
    assert response["success"] is False
    assert str(response["status"]) == "400"
    assert response["message"] == "Note ID must be a valid ID"

    # Volta à tela inicial
    driver.press_keycode(4)
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="com.ab.apiclient:id/design_menu_item_text" and @text="New Request"]'))).click()

    # Cleanup
    delete_user(driver, random_number)

    sleep(5)

    delete_json_file(random_number)

def test_delete_note_ur(driver):
    # Gerando dados aleatórios para o usuário
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user(driver, random_number)
    log_in_user(driver, random_number)
    create_note(driver, random_number)

    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_token = data['user_token']

    # Dados da nota armazenados no JSON após a criação
    note_id = data['note_id']

    wait = WebDriverWait(driver, 20)

    # Seleciona método HTTP (DELETE)
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="DELETE"]'))).click()

    # Insere a URL com o ID da nota
    delete_note_url = f"https://practice.expandtesting.com/notes/api/notes/{note_id}"
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys(delete_note_url)

    # Adiciona headers obrigatórios
    add_accept_header(driver)
    add_token_header_unauthorized(driver, random_number)

    # Envia requisição
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # Visualiza aba "Raw"
    # wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")'))).click()
    # wait_for_result_element_and_close_ad(driver)
    response_text_element = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/tvResult")
    response_str = response_text_element.text
    response = json.loads(response_str)

    # Valida resposta principal
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