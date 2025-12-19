@echo off
echo ============================================================
echo Appium 서버 시작 (Chromedriver 자동 다운로드 활성화)
echo ============================================================
echo.

REM Android SDK 환경 변수 설정
set ANDROID_HOME=C:\Users\siwoo\AppData\Local\Android\Sdk
set ANDROID_SDK_ROOT=C:\Users\siwoo\AppData\Local\Android\Sdk
set PATH=%ANDROID_HOME%\platform-tools;%ANDROID_HOME%\tools;%PATH%

echo ✓ ANDROID_HOME: %ANDROID_HOME%
echo ✓ ANDROID_SDK_ROOT: %ANDROID_SDK_ROOT%
echo.

appium --allow-insecure=uiautomator2:chromedriver_autodownload

echo.
echo Appium 서버가 종료되었습니다.
pause
