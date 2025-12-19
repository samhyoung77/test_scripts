# requirements.txt
# Appium-Python-Client

from appium import webdriver
from appium.options.android import UiAutomator2Options

# Desired Capabilities 설정
options = UiAutomator2Options()
options.platform_name = 'Android'
options.device_name = 'emulator-5554'
options.app = 'path/to/app.apk'

# 드라이버 생성
driver = webdriver.Remote('http://localhost:4723', options=options)

# 테스트 실행
driver.quit()