"""
Appium 간단한 테스트 - Android 디바이스 연결 확인 및 앱 실행
"""

import sys
import io

# Windows 콘솔 인코딩 문제 해결
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
import time

def test_android_device():
    """Android 디바이스 연결 테스트"""

    # Appium 옵션 설정
    options = UiAutomator2Options()
    options.platform_name = 'Android'
    options.automation_name = 'UiAutomator2'
    options.device_name = 'Android'

    # 설정 앱 열기 (Chromedriver 필요 없음)
    options.app_package = 'com.android.settings'
    options.app_activity = '.Settings'

    driver = None

    try:
        print("=" * 60)
        print("Appium 서버에 연결 중...")
        print("=" * 60)

        # Appium 서버 연결
        driver = webdriver.Remote('http://localhost:4723', options=options)

        print("\n✓ Appium 서버 연결 성공!")
        print(f"✓ 세션 ID: {driver.session_id}")

        time.sleep(3)

        # 디바이스 정보 가져오기
        print("\n" + "=" * 60)
        print("디바이스 정보:")
        print("=" * 60)

        print(f"✓ 플랫폼: {driver.capabilities.get('platformName')}")
        print(f"✓ 플랫폼 버전: {driver.capabilities.get('platformVersion')}")
        print(f"✓ 디바이스 모델: {driver.capabilities.get('deviceModel')}")
        print(f"✓ 디바이스 제조사: {driver.capabilities.get('deviceManufacturer')}")
        print(f"✓ 디바이스 이름: {driver.capabilities.get('deviceName')}")

        # 스크린샷 저장
        screenshot_path = "C:\\appium\\device_test_screenshot.png"
        driver.save_screenshot(screenshot_path)
        print(f"\n✓ 스크린샷 저장: {screenshot_path}")

        # 현재 activity
        print(f"\n✓ 현재 Activity: {driver.current_activity}")
        print(f"✓ 현재 Package: {driver.current_package}")

        print("\n" + "=" * 60)
        print("테스트 성공! Appium이 정상 작동합니다.")
        print("=" * 60)

        return True

    except Exception as e:
        print(f"\n❌ 테스트 실행 중 오류 발생:")
        print(f"   오류 타입: {type(e).__name__}")
        print(f"   오류 메시지: {str(e)}")

        if driver:
            try:
                screenshot_path = "C:\\appium\\error_screenshot.png"
                driver.save_screenshot(screenshot_path)
                print(f"\n✓ 오류 스크린샷 저장: {screenshot_path}")
            except:
                pass

        raise

    finally:
        if driver:
            print("\n" + "=" * 60)
            print("테스트 종료 - 드라이버 정리 중...")
            print("=" * 60)
            time.sleep(2)
            driver.quit()
            print("✓ 드라이버 종료 완료")


if __name__ == "__main__":
    print("\n")
    print("=" * 60)
    print("  Android 디바이스 연결 테스트")
    print("=" * 60)
    print("\n")

    try:
        test_android_device()
        print("\n\n✓ 모든 테스트 완료!")
        print("\n다음 단계: Chrome 브라우저 문제 해결을 위해")
        print("아래 명령어를 실행해주세요:")
        print("\n  appium driver update uiautomator2")
        print("  npm install -g appium-chromedriver")

    except KeyboardInterrupt:
        print("\n\n⚠ 사용자에 의해 테스트가 중단되었습니다.")
    except Exception as e:
        print(f"\n\n❌ 테스트 실패: {str(e)}")
