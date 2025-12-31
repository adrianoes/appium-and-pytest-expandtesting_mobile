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
    delete_json_file, 
    add_token_header,
    add_token_header_unauthorized,
    create_user_api,
    login_user_api,
    delete_user_api,
    create_note_api,
    delete_note_api
)

@pytest.fixture
def driver():
    # Appium configuration
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

    # GitHub Actions
    # driver = webdriver.Remote(command_executor="http://localhost:4723/wd/hub", options=options)
    driver = webdriver.Remote(command_executor="http://localhost:4723", options=options)
    # Local
    yield driver
    driver.quit()

def test_create_note(driver):
    # Setup: create user and login via API
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_api(random_number)
    login_user_api(random_number)

    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_token = data['user_token']
    user_id = data['user_id']

    note_title = Faker().sentence(4)
    note_description = Faker().sentence(5)
    note_category = Faker().random_element(elements=('Home', 'Personal', 'Work'))

    increasing_request_response_timeout(driver)

    wait = WebDriverWait(driver, 20)

    # Select HTTP method (POST)
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="POST"]'))).click()

    # Insert endpoint URL
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys("https://practice.expandtesting.com/notes/api/notes")

    # Add required headers
    add_accept_header(driver)
    add_content_type_header(driver)
    add_token_header(driver, random_number)

    # Locate JSON input field
    json_input_field = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/etJSONData")

    # Prepare JSON body with note data
    json_body = f'''{{
        "title": "{note_title}",
        "description": "{note_description}",
        "category": "{note_category}"
    }}'''

    # Insert JSON body into field
    json_input_field.clear()
    json_input_field.send_keys(json_body)

    # Send request
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # View "Raw" tab
    wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")'))).click()
    wait_for_result_element_and_close_ad(driver)
    response_str = driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/tvResult").text
    response = json.loads(response_str)

    # Validate main response
    assert response["success"] is True
    assert str(response["status"]) == "200"
    assert response["message"] == "Note successfully created"

    note_data = response["data"]

    # Validate returned data matches expected
    assert note_data["user_id"] == user_id
    assert note_data["title"] == note_title
    assert note_data["description"] == note_description
    assert note_data["category"] == note_category
    assert note_data["completed"] is False

    # Update JSON with note data
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

    # Return to home screen
    driver.press_keycode(4)
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="com.ab.apiclient:id/design_menu_item_text" and @text="New Request"]'))).click()

    # Cleanup
    delete_note_api(random_number)
    delete_user_api(random_number)

    sleep(5)

    delete_json_file(random_number)

def test_create_note_br(driver):
    # Setup: create user and login via API
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_api(random_number)
    login_user_api(random_number)

    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_token = data['user_token']
    user_id = data['user_id']

    note_title = Faker().sentence(4)
    note_description = Faker().sentence(5)
    note_category = Faker().random_element(elements=('Home', 'Personal', 'Work'))

    increasing_request_response_timeout(driver)

    wait = WebDriverWait(driver, 20)

    # Select HTTP method (POST)
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="POST"]'))).click()

    # Insert endpoint URL
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys("https://practice.expandtesting.com/notes/api/notes")

    # Add required headers
    add_accept_header(driver)
    add_content_type_header(driver)
    add_token_header(driver, random_number)

    # Locate JSON input field
    json_input_field = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/etJSONData")

    # Prepare JSON body with note data
    json_body = f'''{{
        "title": "{note_title}",
        "description": "{note_description}",
        "category": "a"
    }}'''

    # Insert JSON body into field
    json_input_field.clear()
    json_input_field.send_keys(json_body)

    # Send request
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # View result
    response_text_element = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/tvResult")
    response_str = response_text_element.text
    response = json.loads(response_str)

    # Validate main response
    assert response["success"] is False
    assert str(response["status"]) == "400"
    assert response["message"] == "Category must be one of the categories: Home, Work, Personal"

    # Return to home screen
    driver.press_keycode(4)
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="com.ab.apiclient:id/design_menu_item_text" and @text="New Request"]'))).click()

    # Cleanup
    delete_user_api(random_number)

    sleep(5)

    delete_json_file(random_number)

def test_create_note_ur(driver):
    # Setup: create user and login via API
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_api(random_number)
    login_user_api(random_number)

    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_token = data['user_token']
    user_id = data['user_id']

    note_title = Faker().sentence(4)
    note_description = Faker().sentence(5)
    note_category = Faker().random_element(elements=('Home', 'Personal', 'Work'))

    increasing_request_response_timeout(driver)

    wait = WebDriverWait(driver, 20)

    # Select HTTP method (POST)
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="POST"]'))).click()

    # Insert endpoint URL
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys("https://practice.expandtesting.com/notes/api/notes")

    # Add required headers
    add_accept_header(driver)
    add_content_type_header(driver)
    add_token_header_unauthorized(driver, random_number)

    # Locate JSON input field
    json_input_field = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/etJSONData")

    # Prepare JSON body with note data
    json_body = f'''{{
        "title": "{note_title}",
        "description": "{note_description}",
        "category": "{note_category}"
    }}'''

    # Insert JSON body into field
    json_input_field.clear()
    json_input_field.send_keys(json_body)

    # Send request
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # View result
    response_text_element = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/tvResult")
    response_str = response_text_element.text
    response = json.loads(response_str)

    # Validate main response
    assert response["success"] is False
    assert str(response["status"]) == "401"
    assert response["message"] == "Access token is not valid or has expired, you will need to login"

    # Return to home screen
    driver.press_keycode(4)
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="com.ab.apiclient:id/design_menu_item_text" and @text="New Request"]'))).click()

    # Cleanup
    delete_user_api(random_number)

    sleep(5)

    delete_json_file(random_number)

def test_get_notes(driver):
    # Setup: create user and notes via API
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_api(random_number)
    login_user_api(random_number)
    create_note_api(random_number)
    
    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    increasing_request_response_timeout(driver)

    wait = WebDriverWait(driver, 20)

    # Select HTTP method (GET)
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="GET"]'))).click()

    # Insert URL to get all notes
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys("https://practice.expandtesting.com/notes/api/notes")

    # Add headers
    add_accept_header(driver)
    add_token_header(driver, random_number)

    # Send request
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # View "Raw" tab
    wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")'))).click()
    wait_for_result_element_and_close_ad(driver)
    response_str = driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/tvResult").text
    response = json.loads(response_str)

    # Validate main response
    assert response["success"] is True
    assert str(response["status"]) == "200"
    assert response["message"] == "Notes successfully retrieved"

    notes = response["data"]
    assert len(notes) == 1  # Should return one note

    # Read expected data from JSON file
    user_id = data["user_id"]

    # --- Note 1 (index 0) ---
    note_1 = notes[0]
    assert note_1["id"] == data["note_id"]
    assert note_1["user_id"] == user_id
    assert note_1["title"] == data["note_title"]
    assert note_1["description"] == data["note_description"]
    assert note_1["category"] == data["note_category"]
    assert note_1["completed"] == data["note_completed"]
    assert note_1["created_at"] == data["note_created_at"]
    assert note_1["updated_at"] == data["note_updated_at"]

    # Return to home screen
    driver.press_keycode(4)
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="com.ab.apiclient:id/design_menu_item_text" and @text="New Request"]'))).click()

    # Cleanup
    delete_note_api(random_number)
    delete_user_api(random_number)

    sleep(5)

    delete_json_file(random_number)

def test_get_notes_ur(driver):
    # Setup: create user and notes via API
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_api(random_number)
    login_user_api(random_number)
    create_note_api(random_number)
    
    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    increasing_request_response_timeout(driver)

    wait = WebDriverWait(driver, 20)

    # Select HTTP method (GET)
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="GET"]'))).click()

    # Insert URL to get all notes
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys("https://practice.expandtesting.com/notes/api/notes")

    # Add headers
    add_accept_header(driver)
    add_token_header_unauthorized(driver, random_number)

    # Send request
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # View "Raw" tab
    response_text_element = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/tvResult")
    response_str = response_text_element.text
    response = json.loads(response_str)

    # Validate main response
    assert response["success"] is False
    assert str(response["status"]) == "401"
    assert response["message"] == "Access token is not valid or has expired, you will need to login"

    # Return to home screen
    driver.press_keycode(4)
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="com.ab.apiclient:id/design_menu_item_text" and @text="New Request"]'))).click()

    # Cleanup
    delete_note_api(random_number)
    delete_user_api(random_number)

    sleep(5)

    delete_json_file(random_number)

def test_get_note(driver):
    # Setup: create user and note via API
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_api(random_number)
    login_user_api(random_number)
    create_note_api(random_number)

    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_token = data['user_token']
    user_id = data['user_id']

    # Note data stored in JSON after creation
    note_id = data['note_id']
    note_title = data['note_title']
    note_description = data['note_description']
    note_category = data['note_category']
    note_completed = data['note_completed']
    note_created_at = data['note_created_at']
    increasing_request_response_timeout(driver)

    note_updated_at = data['note_updated_at']

    wait = WebDriverWait(driver, 20)

    # Select HTTP method (GET)
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="GET"]'))).click()

    # Insert URL with note ID
    get_note_url = f"https://practice.expandtesting.com/notes/api/notes/{note_id}"
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys(get_note_url)

    # Add required headers
    add_accept_header(driver)
    add_token_header(driver, random_number)

    # Send request
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # View "Raw" tab
    wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")'))).click()
    wait_for_result_element_and_close_ad(driver)
    response_str = driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/tvResult").text
    response = json.loads(response_str)

    # Validate main response
    assert response["success"] is True
    assert str(response["status"]) == "200"
    assert response["message"] == "Note successfully retrieved"

    # Validate returned data
    note_data = response["data"]
    assert note_data["id"] == note_id
    assert note_data["user_id"] == user_id
    assert note_data["title"] == note_title
    assert note_data["description"] == note_description
    assert note_data["category"] == note_category
    assert note_data["completed"] == note_completed
    assert note_data["created_at"] == note_created_at
    assert note_data["updated_at"] == note_updated_at

    # Return to home screen
    driver.press_keycode(4)
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="com.ab.apiclient:id/design_menu_item_text" and @text="New Request"]'))).click()

    # Cleanup
    delete_note_api(random_number)
    delete_user_api(random_number)

    sleep(5)

    delete_json_file(random_number)

def test_get_note_ur(driver):
    # Setup: create user and note via API
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_api(random_number)
    login_user_api(random_number)
    create_note_api(random_number)

    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_token = data['user_token']
    user_id = data['user_id']

    # Note data stored in JSON after creation
    note_id = data['note_id']
    note_title = data['note_title']
    note_description = data['note_description']
    note_category = data['note_category']
    note_completed = data['note_completed']
    note_created_at = data['note_created_at']
    note_updated_at = data['note_updated_at']

    increasing_request_response_timeout(driver)

    wait = WebDriverWait(driver, 20)

    # Select HTTP method (GET)
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="GET"]'))).click()

    # Insert URL with note ID
    get_note_url = f"https://practice.expandtesting.com/notes/api/notes/{note_id}"
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys(get_note_url)

    # Add required headers
    add_accept_header(driver)
    add_token_header_unauthorized(driver, random_number)

    # Send request
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # View result
    response_text_element = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/tvResult")
    response_str = response_text_element.text
    response = json.loads(response_str)

    # Validate main response
    assert response["success"] is False
    assert str(response["status"]) == "401"
    assert response["message"] == "Access token is not valid or has expired, you will need to login"

    # Return to home screen
    driver.press_keycode(4)
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="com.ab.apiclient:id/design_menu_item_text" and @text="New Request"]'))).click()

    # Cleanup
    delete_note_api(random_number)
    delete_user_api(random_number)

    sleep(5)

    delete_json_file(random_number)

def test_update_note(driver):
    # Setup: create user and note via API
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_api(random_number)
    login_user_api(random_number)
    create_note_api(random_number)

    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_token = data['user_token']
    user_id = data['user_id']

    # Current note data
    note_id = data['note_id']
    note_created_at = data['note_created_at']

    # Generate updated values with Faker
    note_updated_title = Faker().sentence(4)
    increasing_request_response_timeout(driver)

    note_updated_description = Faker().sentence(5)
    note_updated_category = Faker().random_element(elements=('Home', 'Personal', 'Work'))
    note_updated_completed = True

    wait = WebDriverWait(driver, 20)

    # Select HTTP method (PUT)
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="PUT"]'))).click()

    # Insert URL with note ID
    update_note_url = f"https://practice.expandtesting.com/notes/api/notes/{note_id}"
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys(update_note_url)

    # Add required headers
    add_accept_header(driver)
    add_content_type_header(driver)  # application/x-www-form-urlencoded
    add_token_header(driver, random_number)

    # Locate JSON input field
    json_input_field = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/etJSONData")

    # Prepare JSON body with note data
    json_body = f'''{{
        "title": "{note_updated_title}",
        "description": "{note_updated_description}",
        "category": "{note_updated_category}",
        "completed": "{str(note_updated_completed).lower()}"
    }}'''

    # Insert JSON body into field
    json_input_field.clear()
    json_input_field.send_keys(json_body)

    # Send request
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # View "Raw" tab
    wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")'))).click()
    wait_for_result_element_and_close_ad(driver)
    response_str = driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/tvResult").text
    response = json.loads(response_str)

    # Validate main response
    assert response["success"] is True
    assert str(response["status"]) == "200"
    assert response["message"] == "Note successfully Updated"

    note_data = response["data"]

    # Validate updated data
    assert note_data["id"] == note_id
    assert note_data["user_id"] == user_id
    assert note_data["title"] == note_updated_title
    assert note_data["description"] == note_updated_description
    assert note_data["category"] == note_updated_category
    assert note_data["completed"] is True
    assert note_data["created_at"] == note_created_at
    assert note_data["updated_at"] != note_created_at  # updated_at should be different after update

    # Return to home screen
    driver.press_keycode(4)
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="com.ab.apiclient:id/design_menu_item_text" and @text="New Request"]'))).click()

    # Cleanup
    delete_note_api(random_number)
    delete_user_api(random_number)

    sleep(5)

    delete_json_file(random_number)

def test_update_note_br(driver):
    # Setup: create user and note via API
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_api(random_number)
    login_user_api(random_number)
    create_note_api(random_number)

    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_token = data['user_token']
    user_id = data['user_id']

    # Current note data
    note_id = data['note_id']
    note_created_at = data['note_created_at']

    # Generate updated values with Faker
    note_updated_title = Faker().sentence(4)
    note_updated_description = Faker().sentence(5)
    note_updated_category = Faker().random_element(elements=('Home', 'Personal', 'Work'))
    note_updated_completed = True

    increasing_request_response_timeout(driver)

    wait = WebDriverWait(driver, 20)

    # Select HTTP method (PUT)
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="PUT"]'))).click()

    # Insert URL with note ID
    update_note_url = f"https://practice.expandtesting.com/notes/api/notes/{note_id}"
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys(update_note_url)

    # Add required headers
    add_accept_header(driver)
    add_content_type_header(driver)  # application/x-www-form-urlencoded
    add_token_header(driver, random_number)

    # Locate JSON input field
    json_input_field = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/etJSONData")

    # Prepare JSON body with invalid category (bad request)
    json_body = f'''{{
        "title": "{note_updated_title}",
        "description": "{note_updated_description}",
        "category": "a",
        "completed": "{str(note_updated_completed).lower()}"
    }}'''

    # Insert JSON body into field
    json_input_field.clear()
    json_input_field.send_keys(json_body)

    # Send request
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # View result
    response_text_element = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/tvResult")
    response_str = response_text_element.text
    response = json.loads(response_str)

    # Validate main response
    assert response["success"] is False
    assert str(response["status"]) == "400"
    assert response["message"] == "Category must be one of the categories: Home, Work, Personal"

    # Return to home screen
    driver.press_keycode(4)
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="com.ab.apiclient:id/design_menu_item_text" and @text="New Request"]'))).click()

    # Cleanup
    delete_note_api(random_number)
    delete_user_api(random_number)

    sleep(5)

    delete_json_file(random_number)

def test_update_note_ur(driver):
    # Setup: create user and note via API
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_api(random_number)
    login_user_api(random_number)
    create_note_api(random_number)

    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_token = data['user_token']
    user_id = data['user_id']

    # Current note data
    note_id = data['note_id']
    note_created_at = data['note_created_at']

    # Generate updated values with Faker
    note_updated_title = Faker().sentence(4)
    note_updated_description = Faker().sentence(5)
    note_updated_category = Faker().random_element(elements=('Home', 'Personal', 'Work'))
    note_updated_completed = True

    increasing_request_response_timeout(driver)

    wait = WebDriverWait(driver, 20)

    # Select HTTP method (PUT)
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="PUT"]'))).click()

    # Insert URL with note ID
    update_note_url = f"https://practice.expandtesting.com/notes/api/notes/{note_id}"
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys(update_note_url)

    # Add required headers with invalid token
    add_accept_header(driver)
    add_content_type_header(driver)  # application/x-www-form-urlencoded
    add_token_header_unauthorized(driver, random_number)

    # Locate JSON input field
    json_input_field = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/etJSONData")

    # Prepare JSON body with note data
    json_body = f'''{{
        "title": "{note_updated_title}",
        "description": "{note_updated_description}",
        "category": "{note_updated_category}",
        "completed": "{str(note_updated_completed).lower()}"
    }}'''

    # Insert JSON body into field
    json_input_field.clear()
    json_input_field.send_keys(json_body)

    # Send request
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # View result
    response_text_element = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/tvResult")
    response_str = response_text_element.text
    response = json.loads(response_str)

    # Validate main response
    assert response["success"] is False
    assert str(response["status"]) == "401"
    assert response["message"] == "Access token is not valid or has expired, you will need to login"

    # Return to home screen
    driver.press_keycode(4)
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="com.ab.apiclient:id/design_menu_item_text" and @text="New Request"]'))).click()

    # Cleanup
    delete_note_api(random_number)
    delete_user_api(random_number)

    sleep(5)

    delete_json_file(random_number)

def test_update_note_status(driver):
    # Setup: create user and note via API
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_api(random_number)
    login_user_api(random_number)
    create_note_api(random_number)

    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_token = data['user_token']
    user_id = data['user_id']

    # Note data stored in JSON after creation
    note_id = data['note_id']
    note_title = data['note_title']
    note_description = data['note_description']
    note_category = data['note_category']
    note_created_at = data['note_created_at']
    increasing_request_response_timeout(driver)

    note_updated_at = data['note_updated_at']

    note_updated_completed = True

    wait = WebDriverWait(driver, 20)

    # Select HTTP method (PATCH)
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="PATCH"]'))).click()

    # Insert URL with note ID
    update_note_url = f"https://practice.expandtesting.com/notes/api/notes/{note_id}"
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys(update_note_url)

    # Add required headers
    add_accept_header(driver)
    add_content_type_header(driver)  # application/x-www-form-urlencoded
    add_token_header(driver, random_number)

    # Locate JSON input field
    json_input_field = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/etJSONData")

    # Prepare JSON body with note data
    json_body = f'''{{
        "completed": "{str(note_updated_completed).lower()}"
    }}'''

    # Insert JSON body into field
    json_input_field.clear()
    json_input_field.send_keys(json_body)

    # Send request
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # View "Raw" tab
    wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")'))).click()
    wait_for_result_element_and_close_ad(driver)
    response_str = driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/tvResult").text
    response = json.loads(response_str)

    # Validate main response
    assert response["success"] is True
    assert str(response["status"]) == "200"
    assert response["message"] == "Note successfully Updated"

    note_data = response["data"]

    # Validate updated data
    assert note_data["id"] == note_id
    assert note_data["user_id"] == user_id
    assert note_data["title"] == note_title
    assert note_data["description"] == note_description
    assert note_data["category"] == note_category
    assert note_data["completed"] is True
    assert note_data["created_at"] == note_created_at
    assert note_data["updated_at"] != note_updated_at  # updated_at should be different after update

    # Return to home screen
    driver.press_keycode(4)
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="com.ab.apiclient:id/design_menu_item_text" and @text="New Request"]'))).click()

    # Cleanup
    delete_note_api(random_number)
    delete_user_api(random_number)

    sleep(5)

    delete_json_file(random_number)

def test_update_note_status_br(driver):
    # Setup: create user and note via API
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_api(random_number)
    login_user_api(random_number)
    create_note_api(random_number)

    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_token = data['user_token']
    user_id = data['user_id']

    # Note data stored in JSON after creation
    note_id = data['note_id']
    note_title = data['note_title']
    note_description = data['note_description']
    note_category = data['note_category']
    note_created_at = data['note_created_at']
    note_updated_at = data['note_updated_at']

    note_updated_completed = True

    increasing_request_response_timeout(driver)

    wait = WebDriverWait(driver, 20)

    # Select HTTP method (PATCH)
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="PATCH"]'))).click()

    # Insert URL with note ID
    update_note_url = f"https://practice.expandtesting.com/notes/api/notes/{note_id}"
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys(update_note_url)

    # Add required headers
    add_accept_header(driver)
    add_content_type_header(driver)  # application/x-www-form-urlencoded
    add_token_header(driver, random_number)

    # Locate JSON input field
    json_input_field = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/etJSONData")

    # Prepare JSON body with note data
    json_body = f'''{{
        "completed": "a"
    }}'''

    # Insert JSON body into field
    json_input_field.clear()
    json_input_field.send_keys(json_body)

    # Send request
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # View result
    response_text_element = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/tvResult")
    response_str = response_text_element.text
    response = json.loads(response_str)

    # Validate main response
    assert response["success"] is False
    assert str(response["status"]) == "400"
    assert response["message"] == "Note completed status must be boolean"

    # Return to home screen
    driver.press_keycode(4)
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="com.ab.apiclient:id/design_menu_item_text" and @text="New Request"]'))).click()

    # Cleanup
    delete_note_api(random_number)
    delete_user_api(random_number)

    sleep(5)

    delete_json_file(random_number)

def test_update_note_status_ur(driver):
    # Setup: create user and note via API
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_api(random_number)
    login_user_api(random_number)
    create_note_api(random_number)

    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_token = data['user_token']
    user_id = data['user_id']

    # Note data stored in JSON after creation
    note_id = data['note_id']
    note_title = data['note_title']
    note_description = data['note_description']
    note_category = data['note_category']
    note_created_at = data['note_created_at']
    note_updated_at = data['note_updated_at']

    note_updated_completed = True

    increasing_request_response_timeout(driver)

    wait = WebDriverWait(driver, 20)

    # Select HTTP method (PUT)
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="PATCH"]'))).click()

    # Insert URL with note ID
    update_note_url = f"https://practice.expandtesting.com/notes/api/notes/{note_id}"
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys(update_note_url)

    # Add required headers
    add_accept_header(driver)
    add_content_type_header(driver)  # application/x-www-form-urlencoded
    add_token_header_unauthorized(driver, random_number)

    # Locate JSON input field
    json_input_field = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/etJSONData")

    # Prepare JSON body with note data
    json_body = f'''{{
        "completed": "{note_updated_completed}"
    }}'''

    # Insert JSON body into field
    json_input_field.clear()
    json_input_field.send_keys(json_body)

    # Send request
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # View "Raw" tab
    # wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")'))).click()
    # wait_for_result_element_and_close_ad(driver)
    response_text_element = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/tvResult")
    response_str = response_text_element.text
    response = json.loads(response_str)

    # Validate main response
    assert response["success"] is False
    assert str(response["status"]) == "401"
    assert response["message"] == "Access token is not valid or has expired, you will need to login"

    # Return to home screen
    driver.press_keycode(4)
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="com.ab.apiclient:id/design_menu_item_text" and @text="New Request"]'))).click()

    # Cleanup
    delete_note_api(random_number)
    delete_user_api(random_number)

    sleep(5)

    delete_json_file(random_number)

def test_delete_note(driver):
    # Setup: create user and note via API
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_api(random_number)
    login_user_api(random_number)
    create_note_api(random_number)

    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_token = data['user_token']

    # Note data stored in JSON after creation
    note_id = data['note_id']

    increasing_request_response_timeout(driver)

    wait = WebDriverWait(driver, 20)

    # Select HTTP method (DELETE)
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="DELETE"]'))).click()

    # Insert URL with note ID
    delete_note_url = f"https://practice.expandtesting.com/notes/api/notes/{note_id}"
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys(delete_note_url)

    # Add required headers
    add_accept_header(driver)
    add_token_header(driver, random_number)

    # Send request
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # View "Raw" tab
    wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")'))).click()
    wait_for_result_element_and_close_ad(driver)
    response_str = driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/tvResult").text
    response = json.loads(response_str)

    # Validate main response
    assert response["success"] is True
    assert str(response["status"]) == "200"
    assert response["message"] == "Note successfully deleted"

    # Remove note data from local JSON
    for key in list(data.keys()):
        if key.startswith("note_"):
            del data[key]

    with open(filepath, 'w') as file:
        json.dump(data, file)

    # Return to home screen
    driver.press_keycode(4)
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="com.ab.apiclient:id/design_menu_item_text" and @text="New Request"]'))).click()

    # Cleanup
    delete_user_api(random_number)

    sleep(5)

    delete_json_file(random_number)

def test_delete_note_br(driver):
    # Setup: create user and note via API
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_api(random_number)
    login_user_api(random_number)
    create_note_api(random_number)

    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_token = data['user_token']

    # Note data stored in JSON after creation
    note_id = data['note_id']

    increasing_request_response_timeout(driver)

    wait = WebDriverWait(driver, 20)

    # Select HTTP method (DELETE)
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="DELETE"]'))).click()

    # Insert URL with note ID
    delete_note_url = f"https://practice.expandtesting.com/notes/api/notes/@{note_id}"
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys(delete_note_url)

    # Add required headers
    add_accept_header(driver)
    add_token_header(driver, random_number)

    # Send request
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # View result
    response_text_element = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/tvResult")
    response_str = response_text_element.text
    response = json.loads(response_str)

    # Validate main response
    assert response["success"] is False
    assert str(response["status"]) == "400"
    assert response["message"] == "Note ID must be a valid ID"

    # Return to home screen
    driver.press_keycode(4)
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="com.ab.apiclient:id/design_menu_item_text" and @text="New Request"]'))).click()

    # Cleanup
    delete_note_api(random_number)
    delete_user_api(random_number)

    sleep(5)

    delete_json_file(random_number)

def test_delete_note_ur(driver):
    # Setup: create user and note via API
    random_number = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_api(random_number)
    login_user_api(random_number)
    create_note_api(random_number)

    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_token = data['user_token']

    # Note data stored in JSON after creation
    note_id = data['note_id']

    increasing_request_response_timeout(driver)

    wait = WebDriverWait(driver, 20)

    # Select HTTP method (DELETE)
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="DELETE"]'))).click()

    # Insert URL with note ID
    delete_note_url = f"https://practice.expandtesting.com/notes/api/notes/{note_id}"
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys(delete_note_url)

    # Add required headers
    add_accept_header(driver)
    add_token_header_unauthorized(driver, random_number)

    # Send request
    driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()

    # View result
    response_text_element = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/tvResult")
    response_str = response_text_element.text
    response = json.loads(response_str)

    # Validate main response
    assert response["success"] is False
    assert str(response["status"]) == "401"
    assert response["message"] == "Access token is not valid or has expired, you will need to login"

    # Return to home screen
    driver.press_keycode(4)
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton"))).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="com.ab.apiclient:id/design_menu_item_text" and @text="New Request"]'))).click()

    # Cleanup
    delete_note_api(random_number)
    delete_user_api(random_number)

    sleep(5)

    delete_json_file(random_number)