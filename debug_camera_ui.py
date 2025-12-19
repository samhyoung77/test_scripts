"""
카메라 앱의 UI 요소를 확인하는 디버그 스크립트
"""
from appium import webdriver
from appium.options.android import UiAutomator2Options
import time

options = UiAutomator2Options()
options.platform_name = 'Android'
options.app_package = 'com.google.android.GoogleCamera'
options.app_activity = 'com.android.camera.CameraLauncher'
options.new_command_timeout = 300
options.no_reset = True
options.auto_grant_permissions = True
options.set_capability("skipServerInstallation", True)
options.set_capability("noSign", True)

driver = webdriver.Remote('http://localhost:4723', options=options)
print("✓ Appium 세션 연결 성공\n")

time.sleep(3)

print("=" * 60)
print("현재 화면의 모든 UI 요소 검색 중...")
print("=" * 60)

# 페이지 소스 가져오기
page_source = driver.page_source

# 'video' 또는 'mode' 관련 요소 찾기
import re
video_elements = re.findall(r'resource-id="([^"]*(?:video|mode|더보기|more)[^"]*)"', page_source, re.IGNORECASE)
print("\n📹 비디오/모드 관련 요소:")
for elem in set(video_elements):
    print(f"  - {elem}")

# text 속성에서 찾기
text_elements = re.findall(r'text="([^"]*(?:동영상|비디오|video|더보기|more)[^"]*)"', page_source, re.IGNORECASE)
print("\n📝 텍스트 관련 요소:")
for elem in set(text_elements):
    print(f"  - {elem}")

# content-desc에서 찾기
desc_elements = re.findall(r'content-desc="([^"]*(?:동영상|비디오|video|더보기|more|mode)[^"]*)"', page_source, re.IGNORECASE)
print("\n📋 Content-desc 관련 요소:")
for elem in set(desc_elements):
    print(f"  - {elem}")

# 전체 페이지 소스를 파일로 저장
with open('/Users/chosamhyeong/appium/page_source.xml', 'w', encoding='utf-8') as f:
    f.write(page_source)
print("\n💾 전체 페이지 소스 저장: /Users/chosamhyeong/appium/page_source.xml")

driver.quit()
print("\n✓ 완료")
