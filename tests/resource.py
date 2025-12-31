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
import requests

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

# DEPRECATED: Use login_user_api() instead (faster, no ads)
# def log_in_user(driver, random_number):
#     filepath = f"tests/fixtures/testdata-{random_number}.json"
#     with open(filepath, 'r') as file:
#         data = json.load(file)
#
#     user_email = data['user_email']
#     user_password = data['user_password']
#     user_id = data['user_id']
#     user_name = data['user_name']
#
#     wait = WebDriverWait(driver, 20)
#
#     wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
#     wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="POST"]'))).click()
#
#     wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys("https://practice.expandtesting.com/notes/api/users/login")
#
#     add_accept_header(driver)
#     add_content_type_header(driver)
#
#     # Localiza o campo de entrada JSON
#     json_input_field = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/etJSONData")
#
#     # Prepara o corpo JSON com os dados das variáveis
#     json_body = f'''{{
#         "email": "{user_email}",
#         "password": "{user_password}"
#     }}'''
#
#     # Insere o texto formatado no campo
#     json_input_field.send_keys(json_body)
#
#     driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()
#
#     wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")'))).click()
#     wait_for_result_element_and_close_ad(driver)
#     response_str = driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/tvResult").text
#     response = json.loads(response_str)
#
#     assert response["success"] is True
#     assert str(response["status"]) == "200"
#     assert response["message"] == "Login successful"
#     assert response["data"]["id"] == user_id
#     assert response["data"]["name"] == user_name
#     assert response["data"]["email"] == user_email
#
#     user_token = response["data"]["token"]
#     data["user_token"] = user_token
#
#
#     with open(filepath, 'w') as file:
#         json.dump(data, file)
#
#     driver.press_keycode(4)
#     wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton"))).click()
#     wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="com.ab.apiclient:id/design_menu_item_text" and @text="New Request"]'))).click()

# DEPRECATED: Use delete_user_api() instead (faster, no ads)
# def delete_user(driver, random_number):
#     filepath = f"tests/fixtures/testdata-{random_number}.json"
#     with open(filepath, 'r') as file:
#         data = json.load(file)
#
#     user_token = data['user_token']
#     wait = WebDriverWait(driver, 20)
#
#     wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
#     wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="DELETE"]'))).click()
#
#     wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys("https://practice.expandtesting.com/notes/api/users/delete-account")
#
#     add_accept_header(driver)
#     add_token_header(driver, random_number)
#
#     driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()
#
#     wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")'))).click()
#     wait_for_result_element_and_close_ad(driver)
#     response_str = driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/tvResult").text
#     response = json.loads(response_str)
#
#     assert response["success"] is True
#     assert str(response["status"]) == "200"
#     assert response["message"] == "Account successfully deleted"
#
#     driver.press_keycode(4)
#     wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton"))).click()
#     wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="com.ab.apiclient:id/design_menu_item_text" and @text="New Request"]'))).click()

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
    # Implement here according to ad behavior
    pass

def add_token_header(driver, random_number):
    filepath = f"tests/fixtures/testdata-{random_number}.json"
    with open(filepath, 'r') as file:
        data = json.load(file)

    user_token = data['user_token']

    wait = WebDriverWait(driver, 20)

    # Open header panel
    wait.until(EC.visibility_of_element_located((
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.widget.ImageView").instance(0)'
    ))).click()

    # Fill header with key and token
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

    # Open header panel
    wait.until(EC.visibility_of_element_located((
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.widget.ImageView").instance(0)'
    ))).click()

    # Fill header with key and invalid token
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

# DEPRECATED: Use create_user_api() instead (faster, no ads)
# def create_user(driver, random_number):
#     user_name = Faker().name()
#     user_email = Faker().lexify(text='??').lower() + Faker().company_email().replace("-", "")
#     user_password = Faker().password(length=12, special_chars=False, digits=True, upper_case=True, lower_case=True)
#
#     # Disable WiFi
#     run(["adb", "shell", "svc", "wifi", "disable"])
#
#     sleep(5)
#
#     # Increase timeout values
#     increasing_request_response_timeout(driver)
#
#     # Select HTTP method (POST)
#     sp_http_method = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod")
#     sp_http_method.click()
#     post_method = wait_until_element_visible(driver, AppiumBy.XPATH, "//android.widget.CheckedTextView[@resource-id='android:id/text1' and @text='POST']")
#     post_method.click()
#
#     # Insert base URL
#     url_input = wait_until_element_visible(driver, AppiumBy.XPATH, "//android.widget.EditText[@resource-id='com.ab.apiclient:id/etUrl']")
#     url_input.send_keys("https://practice.expandtesting.com/notes/api/users/register")
#
#     # Add headers
#     add_accept_header(driver)
#     add_content_type_header(driver)
#
#     # Locate JSON input field
#     json_input_field = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/etJSONData")
#
#     # Prepare JSON body with variable data
#     json_body = f'''{{
#         "name": "{user_name}",
#         "email": "{user_email}",
#         "password": "{user_password}"
#     }}'''
#
#     # Insert formatted text into field
#     json_input_field.send_keys(json_body)
#
#     # Send request
#     driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()
#
#     # Open "Raw" tab to view result
#     raw_button = wait_until_element_visible(driver, AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")')
#     raw_button.click()
#
#     # Wait for result and close ad if necessary
#     wait_for_result_element_and_close_ad(driver)
#
#     # Capture response text
#     response_text_element = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/tvResult")
#     response_str = response_text_element.text
#     print(f"string response is: {response_str}")
#
#     # Process JSON response
#     response_json = json.loads(response_str)
#
#     success = response_json.get("success")
#     status = response_json.get("status")
#     message = response_json.get("message")
#
#     # Assertions
#     assert success is True
#     assert str(status) == "201"
#     assert message == "User account created successfully"
#
#     # Create JSON file
#     with open(f"tests/fixtures/testdata-{random_number}.json", "w") as f:
#         json.dump({
#             "user_email": user_email,
#             "user_id": response_json['data']['id'],
#             "user_name": user_name,
#             "user_password": user_password
#         }, f)
#
#     # Press back key to return to home screen and create new request
#     driver.press_keycode(4)
#     wait_until_element_visible(driver, AppiumBy.XPATH, "//android.widget.ImageButton")
#     driver.find_element(AppiumBy.XPATH, "//android.widget.ImageButton").click()
#     wait_until_element_visible(driver, AppiumBy.XPATH, "//android.widget.CheckedTextView[@resource-id='com.ab.apiclient:id/design_menu_item_text' and @text='New Request']")
#     driver.find_element(AppiumBy.XPATH, "//android.widget.CheckedTextView[@resource-id='com.ab.apiclient:id/design_menu_item_text' and @text='New Request']").click()

# DEPRECATED: Use create_note_api() instead (faster, no ads)  
# def create_note(driver, random_number):
#     filepath = f"tests/fixtures/testdata-{random_number}.json"
#     with open(filepath, 'r') as file:
#         data = json.load(file)
#
#     user_token = data['user_token']
#     user_id = data['user_id']
#
#     note_title = Faker().sentence(4)
#     note_description = Faker().sentence(5)
#     note_category = Faker().random_element(elements=('Home', 'Personal', 'Work'))
#
#     wait = WebDriverWait(driver, 20)
#
#     # Select HTTP method (POST)
#     wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
#     wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="POST"]'))).click()
#
#     # Insert endpoint URL
#     wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys("https://practice.expandtesting.com/notes/api/notes")
#
#     # Add required headers
#     add_accept_header(driver)
#     add_content_type_header(driver)
#     add_token_header(driver, random_number)
#
#     # Locate JSON input field
#     json_input_field = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/etJSONData")
#
#     # Prepare JSON body with note data
#     json_body = f'''{{
#         "title": "{note_title}",
#         "description": "{note_description}",
#         "category": "{note_category}"
#     }}'''
#
#     # Insert JSON body into field
#     json_input_field.clear()
#     json_input_field.send_keys(json_body)
#
#     # Send request
#     driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()
#
#     # View "Raw" tab
#     wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")'))).click()
#     wait_for_result_element_and_close_ad(driver)
#     response_str = driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/tvResult").text
#     response = json.loads(response_str)
#
#     # Validate main response
#     assert response["success"] is True
#     assert str(response["status"]) == "200"
#     assert response["message"] == "Note successfully created"
#
#     note_data = response["data"]
#
#     # Validate returned data matches expected
#     assert note_data["user_id"] == user_id
#     assert note_data["title"] == note_title
#     assert note_data["description"] == note_description
#     assert note_data["category"] == note_category
#     assert note_data["completed"] is False
#
#     # Update JSON with note data
#     data.update({
#         "note_id": note_data["id"],
#         "note_title": note_data["title"],
#         "note_description": note_data["description"],
#         "note_category": note_data["category"],
#         "note_completed": note_data["completed"],
#         "note_created_at": note_data["created_at"],
#         "note_updated_at": note_data["updated_at"]
#     })
#
#     with open(filepath, 'w') as file:
#         json.dump(data, file)
#
#     # Return to home screen
#     driver.press_keycode(4)
#     wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton"))).click()
#     wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="com.ab.apiclient:id/design_menu_item_text" and @text="New Request"]'))).click()

# DEPRECATED: Use create_note_api() instead (faster, no ads)
# def create_2nd_note(driver, random_number):
#     filepath = f"tests/fixtures/testdata-{random_number}.json"
#     with open(filepath, 'r') as file:
#         data = json.load(file)
#
#     user_token = data['user_token']
#     user_id = data['user_id']
#
#     note_title_2 = Faker().sentence(4)
#     note_description_2 = Faker().sentence(5)
#     note_category_2 = Faker().random_element(elements=('Home', 'Personal', 'Work'))
#
#     wait = WebDriverWait(driver, 20)
#
#     # Select HTTP method (POST)
#     wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ab.apiclient:id/spHttpMethod"))).click()
#     wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="POST"]'))).click()
#
#     # Insert endpoint URL
#     wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.ab.apiclient:id/etUrl"]'))).send_keys("https://practice.expandtesting.com/notes/api/notes")
#
#     # Add required headers
#     add_accept_header(driver)
#     add_content_type_header(driver)
#     add_token_header(driver, random_number)
#
#     # Locate JSON input field
#     json_input_field = wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/etJSONData")
#
#     # Prepare JSON body with note data
#     json_body = f'''{{
#         "title": "{note_title_2}",
#         "description": "{note_description_2}",
#         "category": "{note_category_2}"
#     }}'''
#
#     # Insert JSON body into field
#     json_input_field.clear()
#     json_input_field.send_keys(json_body)
#
#     # Send request
#     driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/btnSend").click()
#
#     # View "Raw" tab
#     wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Raw")'))).click()
#     wait_for_result_element_and_close_ad(driver)
#     response_str = driver.find_element(AppiumBy.ID, "com.ab.apiclient:id/tvResult").text
#     response = json.loads(response_str)
#
#     # Validate main response
#     assert response["success"] is True
#     assert str(response["status"]) == "200"
#     assert response["message"] == "Note successfully created"
#
#     note_data = response["data"]
#
#     # Validate returned data matches expected
#     assert note_data["user_id"] == user_id
#     assert note_data["title"] == note_title_2
#     assert note_data["description"] == note_description_2
#     assert note_data["category"] == note_category_2
#     assert note_data["completed"] is False
#
#     # Update JSON with second note data
#     data.update({
#         "note_id_2": note_data["id"],
#         "note_title_2": note_data["title"],
#         "note_description_2": note_data["description"],
#         "note_category_2": note_data["category"],
#         "note_completed_2": note_data["completed"],
#         "note_created_at_2": note_data["created_at"],
#         "note_updated_at_2": note_data["updated_at"]
#     })
#
#     with open(filepath, 'w') as file:
#         json.dump(data, file)
#
#     # Return to home screen
#     driver.press_keycode(4)
#     wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton"))).click()
#     wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="com.ab.apiclient:id/design_menu_item_text" and @text="New Request"]'))).click()


# ========== API-based Custom Commands (using requests library) ==========
# These commands are used to reduce test execution time by avoiding ads
# Setup and teardown operations are done via API, only the main action is done via UI

def create_user_api(random_number):
    """Create user via API request"""
    user_name = Faker().name()
    user_email = Faker().lexify(text='??').lower() + Faker().company_email().replace("-", "")
    user_password = Faker().password(length=12, special_chars=False, digits=True, upper_case=True, lower_case=True)

    body = {
        'confirmPassword': user_password,
        'email': user_email,
        'name': user_name,
        'password': user_password
    }
    headers = {'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
    resp = requests.post("https://practice.expandtesting.com/notes/api/users/register", headers=headers, data=body)
    respJS = resp.json()

    assert respJS['success'] is True
    assert respJS['status'] == 201
    assert respJS['message'] == "User account created successfully"

    # Store user data in JSON file
    with open(f"tests/fixtures/testdata-{random_number}.json", 'w') as f:
        json.dump({
            'user_email': user_email,
            'user_id': respJS['data']['id'],
            'user_name': user_name,
            'user_password': user_password
        }, f)


def login_user_api(random_number):
    """Login user via API request and store token"""
    with open(f"tests/fixtures/testdata-{random_number}.json", 'r') as f:
        data = json.load(f)

    user_email = data['user_email']
    user_password = data['user_password']

    body = {'email': user_email, 'password': user_password}
    headers = {'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
    resp = requests.post("https://practice.expandtesting.com/notes/api/users/login", headers=headers, data=body)
    respJS = resp.json()

    assert respJS['success'] is True
    assert respJS['status'] == 200
    assert respJS['message'] == "Login successful"

    # Update JSON with token
    data['user_token'] = respJS['data']['token']
    with open(f"tests/fixtures/testdata-{random_number}.json", 'w') as f:
        json.dump(data, f)


def delete_user_api(random_number):
    """Delete user via API request"""
    with open(f"tests/fixtures/testdata-{random_number}.json", 'r') as f:
        data = json.load(f)

    user_token = data['user_token']
    headers = {'accept': 'application/json', 'x-auth-token': user_token}
    resp = requests.delete("https://practice.expandtesting.com/notes/api/users/delete-account", headers=headers)
    respJS = resp.json()

    assert respJS['success'] is True
    assert respJS['status'] == 200
    assert respJS['message'] == "Account successfully deleted"


def create_note_api(random_number):
    """Create note via API request"""
    with open(f"tests/fixtures/testdata-{random_number}.json", 'r') as f:
        data = json.load(f)

    user_token = data['user_token']
    user_id = data['user_id']

    note_title = Faker().sentence(4)
    note_description = Faker().sentence(5)
    note_category = Faker().random_element(elements=('Home', 'Personal', 'Work'))

    body = {
        'category': note_category,
        'description': note_description,
        'title': note_title
    }
    headers = {'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded', 'x-auth-token': user_token}
    resp = requests.post("https://practice.expandtesting.com/notes/api/notes", headers=headers, data=body)
    respJS = resp.json()

    assert respJS['success'] is True
    assert respJS['status'] == 200
    assert respJS['message'] == "Note successfully created"

    note_data = respJS['data']
    # Update JSON with note data
    data.update({
        'note_id': note_data['id'],
        'note_title': note_data['title'],
        'note_description': note_data['description'],
        'note_category': note_data['category'],
        'note_completed': note_data['completed'],
        'note_created_at': note_data['created_at'],
        'note_updated_at': note_data['updated_at']
    })
    with open(f"tests/fixtures/testdata-{random_number}.json", 'w') as f:
        json.dump(data, f)


def delete_note_api(random_number):
    """Delete note via API request"""
    with open(f"tests/fixtures/testdata-{random_number}.json", 'r') as f:
        data = json.load(f)

    user_token = data['user_token']
    note_id = data['note_id']

    headers = {'accept': 'application/json', 'x-auth-token': user_token}
    resp = requests.delete(f"https://practice.expandtesting.com/notes/api/notes/{note_id}", headers=headers)
    respJS = resp.json()

    assert respJS['success'] is True
    assert respJS['status'] == 200
    assert respJS['message'] == "Note successfully deleted"






