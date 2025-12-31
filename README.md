# appium-and-pytest-expandtesting_api_and_mobile

UI testing in ApiClient apk using [expandtesting](https://practice.expandtesting.com/notes/api/api-docs/). This project contains basic examples on how to use Appium and Robot Framework to test UI tests. Good practices such as hooks, custom commands and tags, among others, are used. All the necessary support documentation to develop this project is placed here. 

# Pre-requirements:

| Requirement                     | Version        | Note              |
| :------------------------------ |:---------------| :---------------- |
| Visual Studio Code              | 1.89.1         | -                 |
| Node.js                         | 22.16.0        | -                 |
| Python                          | 3.13.1         | -                 |
| JDK                             | 21             | -                 |
| Android Studio                  | 2025.2.2.8     | -                 |  
| ApiClient apk                   | 2.4.7          | -                 |
| Appium                          | 2.19.0         | -                 |
| Appium Doctor                   | 1.16.2         | -                 |
| Appium Inspector                | 2025.11.1      | -                 |
| uiautomator2 driver             | 4.2.3          | -                 |
| Virtual device                  | Pixel 4        | -                 |
| Virtual device API              | 29             | -                 |
| setuptools                      | 80.90.0        | -                 |
| Appium-Python-Client            | 5.2.4          | -                 |
| Pytest                          | 8.4.1          | -                 |
| Requests                        | 2.32.0         | -                 |
| Faker                           | 37.4.0         | -                 |
| pytest-html                     | 4.1.1          | -                 |
| python-dotenv                   | 1.2.1          | -                 |

# Installation:

- See [Visual Studio Code page](https://code.visualstudio.com/) and install the latest VSC stable version. Keep all the prefereced options as they are until you reach the possibility to check the checkboxes below: 
  - :white_check_mark: **Add "Open with code" action to Windows Explorer file context menu**; 
  - :white_check_mark: **Add "Open with code" action to Windows Explorer directory context menu**.
Check then both to add both options in context menu.
- See [Node.js page](https://nodejs.org/en) and install the aforementioned Node.js version. Keep all the preferenced options as they are.
- See [python page](https://www.python.org/downloads/) and download the latest Python stable version. Start the installation and check the checkboxes below: 
  - :white_check_mark: **Use admin privileges when installing py.exe**, :white_check_mark: **Add python.exe to PATH** and :point_right: **Customize installation**;
  - :point_right: **Next**; 
  - :white_check_mark: **Install Python 3.13 for all users**, set **Customize install location** as **C:\Python313**, click :point_right: **Install**;
  - :point_right: **Yes** to accept changes in the system;
  - :point_right: **Close** after installation is done.
- See [JDK Development Kit 21 downloads](https://www.oracle.com/in/java/technologies/downloads/#jdk21-windows), download the proper version for your OS and install it by keeping the preferenced options. 
- See [Anroid Studio download page](https://developer.android.com/), download the last version and install it by keeping the preferenced options. Open Virtual Device Manager and create an image as simple as possible. 
- Open your terminal in your project directory and execute ```npm init``` to initiate a project.
- Open your terminal in your project directory and execute ```npm i appium``` to install Appium.
- Open your terminal in your project directory and execute ```npm i appium-doctor``` to install Appium Doctor.
- Right click :point_right: **My Computer** and select :point_right: **Properties**. On the :point_right: **Advanced** tab, select :point_right: **Environment Variables**, and then, in System Variables, create a variable named JAVA_HOME to point to where the JDK software is located, for example, C:\Program Files\Java\jdk-21.
- Right click :point_right: **My Computer** and select :point_right: **Properties**. On the :point_right: **Advanced** tab, select :point_right: **Environment Variables**, and then, in System Variables, create a variable named ANDROID_HOME to point to where the sdk software is located, for example, C:\Users\user\AppData\Local\Android\Sdk.
- Right click :point_right: **My Computer** and select :point_right: **Properties**. On the :point_right: **Advanced** tab, select :point_right: **Environment Variables**, and then edit Path system variable with the new %JAVA_HOME%\bin and %ANDROID_HOME%\platform-tools entries.
- Open your terminal in your project directory and execute ```npx appium-doctor --android``` to run Appium Doctor and check Appium instalation status.
- Open your terminal in your project directory and execute ```npx appium driver install uiautomator2``` to install drivers for automationName and platformName capabilities.
- See [Appium Inspector download page](https://github.com/appium/appium-inspector/releases), download and install it. Configure capabilities as below and save it:
  ```
  {
    "platformName": "Android",
    "appium:platformVersion": "10.0",
    "appium:deviceName": "Pixel_4_API_29",
    "appium:automationName": "UIAutomator2",
    "appium:app": "C:\\appium-and-pytest-expandtesting_api_and_mobile\\apps\\apiClient.apk",
    "appium:adbExecTimeout": 120000,
    "appium:autoGrantPermissions": true,
    "appium:appActivity": "com.ab.apiclient.ui.Splash",
    "appium:appWaitActivity": "com.ab.apiclient.ui.Splash,com.ab.apiclient.*,com.ab.apiclient.ui.MainActivity",
    "appium:appWaitDuration": 20000,
    "appium:noReset": true,
    "appium:autoDismissAlerts": true,
    "appium:uiautomator2ServerInstallTimeout": 60000
  }
  ```  
- Open windows prompt as admin and execute ```pip install Appium-Python-Client``` to install Appium Python Client.
- Open windows prompt as admin and execute ```pip install Faker``` to install Faker library.
- Open windows prompt as admin and execute ```pip install requests``` to install Requests library.
- Open windows prompt as admin and execute ```pip install pytest``` to install Pytest.
- Open windows prompt as admin and execute ```pip install python-dotenv``` to install python-dotenv.
- Open windows prompt as admin and execute ```pip install pytest-html``` to install pytest-html plugin.
- Open windows prompt as admin and execute ```pip install setuptools``` to install setuptools package.
- Open your terminal in your project directory and execute ```npx appium``` to start appium session.
- Execute Virtual Device Manager on Android Studio.
- Open Appium Inspector and start the appium session. 

# Tests:

- Execute ```pytest ./tests -v --html=./reports/report.html``` to run tests in verbose mode and generate a report inside reports folder.
- Execute ```pytest ./tests/test_users.py -k create_user -v --html=./reports/report.html``` to run tests that contains "create_user" in its structure inside test_users.py file in verbose mode and generate a report inside reports folder.
- Execute ```pytest ./tests -v --html=./reports/report.html``` to run tests and capture screenshots/videos/logs automatically.
- Execute ```python jira_reporter.py``` to manually create JIRA bugs for failed tests after reviewing results.
- Execute ```python run_tests_with_jira.py``` to run all tests and automatically create JIRA bugs for failures in a single command.
- Execute ```python run_tests_with_jira.py -k create_user``` to run tests matching "create_user" and automatically create JIRA bugs for failures.
- Execute ```python run_tests_with_jira.py -k "login or delete"``` to run tests matching "login" or "delete" and automatically create JIRA bugs for failures.
- Hit :point_right:**Testing** button on left side bar in VSC and choose the tests to execute.

# CI/CD with GitHub Actions:

This project includes automated testing with GitHub Actions that:
- Executes all tests automatically on every push
- Captures screenshots, logs, and HTML reports
- Uploads test artifacts to GitHub (30 days retention)
- Creates JIRA issues automatically for failed tests

## Setup GitHub Actions JIRA Integration:

1. Go to your GitHub repository **Settings** > **Secrets and variables** > **Actions**
2. Add the following repository secrets:
   - `JIRA_BASE_URL` - Your JIRA URL (e.g., `https://yourcompany.atlassian.net`)
   - `JIRA_EMAIL` - Email for JIRA authentication
   - `JIRA_API_SECRET` - JIRA API token ([Get one here](https://id.atlassian.com/manage-profile/security/api-tokens))
   - `JIRA_PROJECT_KEY` - Project key where bugs will be created (e.g., `DEV`)
   - `JIRA_ISSUE_TYPE` - Issue type to create (e.g., `Bug`)

See [.github/GITHUB_SECRETS_SETUP.md](.github/GITHUB_SECRETS_SETUP.md) for detailed setup instructions.

## GitHub Actions Workflow Features:

- ✅ Automatic test execution on push
- ✅ Android emulator setup (Pixel 4 API 29)
- ✅ Screenshot capture on test failures
- ✅ Detailed log generation
- ✅ HTML report generation
- ✅ Artifact upload to GitHub (screenshots, logs, reports)
- ✅ Automatic JIRA issue creation with attachments
- ✅ 30-day artifact retention

## Viewing Test Results:

After each workflow run:
1. Go to **Actions** tab in GitHub
2. Click on the latest workflow run
3. Scroll down to **Artifacts** section
4. Download:
   - `test-artifacts` - Complete test artifacts folder
   - `screenshots` - Test failure screenshots
   - `logs` - Detailed error logs
   - `html-report` - HTML test report

JIRA issues will be created automatically with links in the workflow logs.

# Support:

- [expandtesting API documentation page](https://practice.expandtesting.com/notes/api/api-docs/)
- [expandtesting API demonstration page](https://www.youtube.com/watch?v=bQYvS6EEBZc)
- [Write a Test (Python)](https://appium.io/docs/en/latest/quickstart/test-py/)
- [Quickstart Intro](https://appium.io/docs/en/latest/quickstart/)
- [Download ApiClient : REST API Client APK](https://apiclient-rest-api-client.en.softonic.com/android/download)
- [Atlassian JIRA API Documentation](https://developer.atlassian.com/cloud/jira/platform/rest/v2/)
- [Atlassian API Tokens Management](https://id.atlassian.com/manage-profile/security/api-tokens)
- [ChatGPT](https://chatgpt.com/)
- [Error occured while starting App. Original error: com.abc.xyz.ui.SplashActivity or com.abc.xyz.dev.com.abc.xyz.ui.SplashActivity never started](https://stackoverflow.com/a/48531998)
- [Unable to install APK. Try to increase the 20000ms adb execution timeout represented by 'adbExecTimeout' capability"](https://github.com/appium/appium/issues/12287#issuecomment-1353643684)
- [Unable to resolve host "<URL here>" No address associated with host name [closed]](https://stackoverflow.com/a/31242237)
- [How to turn off Wifi via ADB?](https://stackoverflow.com/a/10038568)
- [how to handle app generated popups in appium](https://stackoverflow.com/a/54970700)

# Tips:

- UI and API tests to send password reset link to user's email and API tests to verify a password reset token and reset a user's password must be tested manually as they rely on e-mail verification. 
- Disable wifi when the apk presents connections problems.
