"""
간단한 카메라 테스트 - UI 요소 디버깅용
"""

import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
import time

options = UiAutomator2Options()
options.platform_name = 'Android'
options.automation_name = 'UiAutomator2'
options.device_name = 'Android'
options.app_package = 'com.google.android.GoogleCamera'
options.app_activity = 'com.android.camera.CameraLauncher'
options.new_command_timeout = 300
options.no_reset = True
options.auto_grant_permissions = True

driver = webdriver.Remote('http://localhost:4723', options=options)

print("\n✓ 카메라 연결 성공!")
time.sleep(3)

# 사진 한 장 촬영 (썸네일이 생기도록)
print("\n사진 촬영 중...")
try:
    shutter = driver.find_element(AppiumBy.ID, 'com.google.android.GoogleCamera:id/shutter_button')
    shutter.click()
    print("✓ 사진 촬영 완료")
    time.sleep(3)
except Exception as e:
    print(f"⚠ 촬영 실패: {e}")

print("\n현재 화면의 클릭 가능한 요소들:")
print("=" * 60)

try:
    # 모든 클릭 가능한 요소 찾기
    clickable = driver.find_elements(AppiumBy.XPATH, "//*[@clickable='true']")

    for idx, elem in enumerate(clickable[:20], 1):
        res_id = elem.get_attribute('resource-id')
        desc = elem.get_attribute('content-desc')
        class_name = elem.get_attribute('class')
        bounds = elem.get_attribute('bounds')

        print(f"\n{idx}. Class: {class_name}")
        if res_id:
            print(f"   Resource-ID: {res_id}")
        if desc:
            print(f"   Content-Desc: {desc}")
        if bounds:
            print(f"   Bounds: {bounds}")

except Exception as e:
    print(f"오류: {str(e)}")

print("\n\n모든 ImageView 요소:")
print("=" * 60)

try:
    images = driver.find_elements(AppiumBy.CLASS_NAME, 'android.widget.ImageView')

    for idx, img in enumerate(images[:10], 1):
        res_id = img.get_attribute('resource-id')
        desc = img.get_attribute('content-desc')
        bounds = img.get_attribute('bounds')
        clickable = img.get_attribute('clickable')

        print(f"\n{idx}. ImageView")
        if res_id:
            print(f"   Resource-ID: {res_id}")
        if desc:
            print(f"   Content-Desc: {desc}")
        if bounds:
            print(f"   Bounds: {bounds}")
        if clickable:
            print(f"   Clickable: {clickable}")

except Exception as e:
    print(f"오류: {str(e)}")

# thumbnail_button 요소 특별 검색
print("\n\n'thumbnail' 관련 요소 특별 검색:")
print("=" * 60)

try:
    # ID로 검색
    thumbnails = driver.find_elements(AppiumBy.XPATH, "//*[contains(@resource-id, 'thumbnail')]")
    print(f"\n✓ 'thumbnail' ID를 포함한 요소: {len(thumbnails)}개")

    for idx, thumb in enumerate(thumbnails[:5], 1):
        res_id = thumb.get_attribute('resource-id')
        desc = thumb.get_attribute('content-desc')
        class_name = thumb.get_attribute('class')
        bounds = thumb.get_attribute('bounds')
        clickable = thumb.get_attribute('clickable')

        print(f"\n  {idx}. {class_name}")
        print(f"     Resource-ID: {res_id}")
        if desc:
            print(f"     Content-Desc: {desc}")
        print(f"     Clickable: {clickable}")
        print(f"     Bounds: {bounds}")

except Exception as e:
    print(f"검색 오류: {str(e)}")

# 스크린샷 저장
screenshot_path = "C:\\appium\\ui_debug.png"
driver.save_screenshot(screenshot_path)
print(f"\n\n✓ 스크린샷 저장: {screenshot_path}")

print("\n테스트 완료. 드라이버 종료...")
driver.quit()
