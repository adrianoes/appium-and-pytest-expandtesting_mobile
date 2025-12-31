# Copilot Instructions for Appium-Pytest-ExpandTesting Mobile

## Quick Start: Understanding the Architecture

This is a **Pytest mobile UI testing framework** that automates REST API calls through the **ApiClient APK** (a REST client app) on Android Pixel 4 emulator (API 29) via Appium/UIAutomator2.

**Key insight**: Tests don't call the API directly—they programmatically interact with the ApiClient UI to make HTTP requests, capture JSON responses, and validate results. This hybrid approach tests the app itself while exercising the real expandtesting.com API.

## Core Components & Data Flow

1. **[tests/resource.py](../tests/resource.py)**: Shared helpers for UI interactions, headers, auth flows, test data persistence
2. **[tests/test_*.py](../tests/)**: Test suites (health, users, notes) with driver fixtures
3. **apps/apiClient.apk**: Android app under test (REST client UI)
4. **tests/fixtures/**: JSON files store per-test credentials and data (random_number indexed)
5. **Appium server**: UIAutomator2 driver on `http://localhost:4723`

**Test flow**: WiFi off → Appium connects → Test creates fake user → Stores JWT in JSON → Reuses token for subsequent requests → Cleanup

## Essential Patterns

### Element Finding & Waits
```python
# All interactions via wait_until_element_visible() with 20s default timeout
wait_until_element_visible(driver, AppiumBy.ID, "com.ab.apiclient:id/etUrl")
# Selector priority: ID → XPATH → CLASS_NAME → ANDROID_UIAUTOMATOR
# ANDROID_UIAUTOMATOR for text: 'new UiSelector().text("Raw")'
```

### UI-Based API Testing Pattern
1. Select HTTP method dropdown (`spHttpMethod`)
2. Enter URL in text field (`etUrl`)
3. Add headers (Accept, Content-Type, x-auth-token) via `add_accept_header()`, `add_content_type_header()`, `add_token_header()`
4. Input JSON body (`etJSONData`)
5. Click send (`btnSend`)
6. Switch to "Raw" tab
7. Parse `tvResult` element text as JSON, assert

### Test Data Lifecycle
- **Generate**: `random_number = Faker().hexify(text='^^^^^^^^^^^^')` + fake user data
- **Persist**: `tests/fixtures/testdata-{random_number}.json` (email, password, user_id, JWT token)
- **Reuse**: Pass `random_number` to `log_in_user()`, `create_note()`, etc.
- **Cleanup**: `delete_json_file(random_number)` at test end

### Special Test Helpers
- `wait_for_result_element_and_close_ad()`: Handles ad overlays by catching timeout
- `increasing_request_response_timeout()`: Sets app timeouts to 120s (Settings UI)
- WiFi disabling: `run(["adb", "shell", "svc", "wifi", "disable"])` before test

## Critical Setup (Run Before Tests)

```bash
# Terminal 1: Start Appium (listens on 4723)
npx appium

# Terminal 2: Launch emulator
# (Pixel 4 API 29 via Android Studio)

# Terminal 3: Run tests
pytest ./tests -v --html=./reports/report.html
```

**Appium options (in fixture):**
- `UiAutomator2Options()` with Pixel_4_API_29, adb_exec_timeout=60000
- `app = "./apps/apiClient.apk"`
- `app_activity = "com.ab.apiclient.ui.Splash"`

## Common Troubleshooting

| Issue | Fix |
|-------|-----|
| App never starts | Increase `adb_exec_timeout` (60000ms) |
| "Element not found" | Ad blocking result—`wait_for_result_element_and_close_ad()` catches this |
| Connection timeout | Call `increasing_request_response_timeout()` at test start |
| Host resolution fails | Disable WiFi: `adb shell svc wifi disable` |
| Selector not found | Use Appium Inspector with saved capabilities; prefer IDs over XPATH |

## Non-Automatable Tests

Password reset flows requiring email verification must be tested manually (no email interception in CI).

## File Map

- [tests/test_health.py](../tests/test_health.py): Basic health check (no auth)
- [tests/test_users.py](../tests/test_users.py): User CRUD, auth, profile updates (30+ test variants with _br/_ur suffixes for bad request/unauthorized)
- [tests/test_notes.py](../tests/test_notes.py): Note CRUD with ownership/auth checks
- [README.md](../README.md): Setup steps, dependency versions, support links
