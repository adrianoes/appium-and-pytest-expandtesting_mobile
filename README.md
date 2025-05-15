# appium-and-pytest-expandtesting_mobile

UI testing in ApiClient apk using [expandtesting](https://practice.expandtesting.com/notes/api/api-docs/). This project contains basic examples on how to use Appium and Robot Framework to test UI tests. Good practices such as hooks, custom commands and tags, among others, are used. All the necessary support documentation to develop this project is placed here. 

# Pre-requirements:

| Requirement                     | Version        | Note                                                            |
| :------------------------------ |:---------------| :-------------------------------------------------------------- |
| Visual Studio Code              | 1.89.1         | -                                                               |
| Node.js                         | 22.11.0        | -                                                               |
| Python                          | 3.13.1         | -                                                               |
| JDK                             | 23             | -                                                               |
| Android Studio                  | 2024.2.1.11    | -                                                               |
| ApiClient apk                   | 2.4.7          | -                                                               |
| Appium                          | 2.16.2         | -                                                               |
| Appium Doctor                   | 1.16.2         | -                                                               |
| Appium Inspector                | 2024.12.1      | -                                                               |
| uiautomator2 driver             | 4.2.3          | -                                                               |
| Virtual device                  | Pixel 4        | -                                                               |
| Virtual device API              | 29             | -                                                               |
| setuptools                      | 75.1.0         | -                                                               | 
| Appium-Python-Client            | 5.1.1          | -                                                               | 
| Pytest                          | 8.3.4          | -                                                               |
| Faker                           | 33.3.1         | -                                                               |
| pytest-html                     | 4.1.1          | -                                                               |

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
- See [JDK Development Kit 23 downloads](https://www.oracle.com/in/java/technologies/downloads/#jdk23-windows), download the proper version for your OS and install it by keeping the preferenced options. 
- See [Anroid Studio download page](https://developer.android.com/), download the last version and install it by keeping the preferenced options. Open Virtual Device Manager and create an image as simple as possible. 
- Open your terminal in your project directory and execute ```npm init``` to initiate a project.
- Open your terminal in your project directory and execute ```npm i appium``` to install Appium.
- Open your terminal in your project directory and execute ```npm i appium-doctor``` to install Appium Doctor.
- Right click :point_right: **My Computer** and select :point_right: **Properties**. On the :point_right: **Advanced** tab, select :point_right: **Environment Variables**, and then edit JAVA_HOME to point to where the JDK software is located, for example, C:\Program Files\Java\jdk-23.
- Right click :point_right: **My Computer** and select :point_right: **Properties**. On the :point_right: **Advanced** tab, select :point_right: **Environment Variables**, and then edit ANDROID_HOME to point to where the sdk software is located, for example, C:\Users\user\AppData\Local\Android\Sdk.
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
    "appium:app": "C:\\appium-and-pytest-expandtesting_mobile\\apps\\apiClient.apk",
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
- Open windows prompt as admin and execute ```pip install pytest``` to install Pytest.
- Open windows prompt as admin and execute ```pip install pytest-html``` to install pytest-html plugin.
- Open windows prompt as admin and execute ```pip install setuptools``` to install setuptools package.
- Open your terminal in your project directory and execute ```npx appium``` to start appium session.
- Execute Virtual Device Manager on Android Studio.
- Open Appium Inspector and start the appium session. 

# Tests:

- Execute ```pytest ./tests -v --html=./reports/report.html``` to run tests in verbose mode and generate a report inside reports folder.
- Execute ```pytest ./tests/api/users_api_test.py -k create_user_api -v --html=./reports/report.html``` to run tests that contains "create_user_api" in its structure inside users_api_test.py file in verbose mode and generate a report inside reports folder.
- Hit :point_right:**Testing** button on left side bar in VSC and choose the tests to execute.

# Support:

- [expandtesting API documentation page](https://practice.expandtesting.com/notes/api/api-docs/)
- [expandtesting API demonstration page](https://www.youtube.com/watch?v=bQYvS6EEBZc)
- [Write a Test (Python)](https://appium.io/docs/en/latest/quickstart/test-py/)
- [Quickstart Intro](https://appium.io/docs/en/latest/quickstart/)
- [Download ApiClient : REST API Client APK](https://apiclient-rest-api-client.en.softonic.com/android/download)
- [ChatGPT](https://chatgpt.com/)
- [Error occured while starting App. Original error: com.abc.xyz.ui.SplashActivity or com.abc.xyz.dev.com.abc.xyz.ui.SplashActivity never started](https://stackoverflow.com/a/48531998)
- [Unable to install APK. Try to increase the 20000ms adb execution timeout represented by 'adbExecTimeout' capability"](https://github.com/appium/appium/issues/12287#issuecomment-1353643684)
- [Unable to resolve host "<URL here>" No address associated with host name [closed]](https://stackoverflow.com/a/31242237)
- [How to turn off Wifi via ADB?](https://stackoverflow.com/a/10038568)
- [how to handle app generated popups in appium](https://stackoverflow.com/a/54970700)

# Tips:

- UI and API tests to send password reset link to user's email and API tests to verify a password reset token and reset a user's password must be tested manually as they rely on e-mail verification. 
- Disable wifi when the apk presents connections problems.
