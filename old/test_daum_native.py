"""
Appium 테스트 스크립트 - Android에서 Native App으로 Daum 접속
(Chromedriver 문제 회피를 위한 대안)
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

def test_daum_with_native_browser():
    """Android Native 브라우저로 Daum 접속"""

    # Appium 옵션 설정
    options = UiAutomator2Options()
    options.platform_name = 'Android'
    options.automation_name = 'UiAutomator2'
    options.device_name = 'Android'

    # 앱 패키지 대신 activity만 사용
    options.app_package = 'com.android.chrome'
    options.app_activity = 'com.google.android.apps.chrome.Main'
    options.no_reset = True

    options.new_command_timeout = 300

    driver = None

    try:
        print("=" * 60)
        print("Appium 서버에 연결 중...")
        print("=" * 60)

        # Appium 서버 연결
        driver = webdriver.Remote('http://localhost:4723', options=options)

        print("\n✓ Appium 서버 연결 성공!")
        print(f"✓ 세션 ID: {driver.session_id}")

        driver.implicitly_wait(10)

        print("\n" + "=" * 60)
        print("Chrome 앱 실행 대기 중...")
        print("=" * 60)

        time.sleep(5)

        # URL 바 찾아서 클릭
        try:
            # Chrome의 URL 바를 찾기 위한 여러 시도
            url_bar_selectors = [
                'com.android.chrome:id/url_bar',
                'com.android.chrome:id/search_box_text',
                '//android.widget.EditText',
            ]

            url_bar = None
            for selector in url_bar_selectors:
                try:
                    if selector.startswith('//'):
                        url_bar = driver.find_element(AppiumBy.XPATH, selector)
                    else:
                        url_bar = driver.find_element(AppiumBy.ID, selector)

                    if url_bar:
                        print(f"\n✓ URL 바 발견: {selector}")
                        break
                except:
                    continue

            if url_bar:
                url_bar.click()
                time.sleep(1)

                # Daum URL 입력
                url_bar.send_keys('www.daum.net')
                time.sleep(1)

                # Enter 키 입력 (키코드 66)
                driver.press_keycode(66)

                print("\n✓ Daum 접속 완료!")

                time.sleep(5)  # 페이지 로딩 대기

                # 현재 activity 확인
                print(f"\n✓ 현재 Activity: {driver.current_activity}")

                # 페이지 소스 가져오기
                page_source = driver.page_source
                print(f"\n✓ 페이지 소스 길이: {len(page_source)} 문자")

                # 뉴스 관련 텍스트 찾기
                if '뉴스' in page_source or 'news' in page_source.lower():
                    print("\n✓ 뉴스 콘텐츠 발견!")

                # 스크린샷 저장
                screenshot_path = "C:\\appium\\daum_native_screenshot.png"
                driver.save_screenshot(screenshot_path)
                print(f"\n✓ 스크린샷 저장: {screenshot_path}")

                # 모든 텍스트 요소 가져오기
                print("\n" + "=" * 60)
                print("페이지 주요 텍스트:")
                print("=" * 60)

                try:
                    text_elements = driver.find_elements(AppiumBy.CLASS_NAME, 'android.widget.TextView')
                    print(f"\n✓ 발견된 텍스트 요소: {len(text_elements)}개\n")

                    for idx, element in enumerate(text_elements[:20], 1):  # 처음 20개만
                        try:
                            text = element.text
                            if text and len(text.strip()) > 0:
                                print(f"{idx}. {text}")
                        except:
                            continue

                except Exception as e:
                    print(f"⚠ 텍스트 추출 오류: {str(e)}")

            else:
                print("\n⚠ URL 바를 찾을 수 없습니다.")
                print("수동으로 브라우저에서 www.daum.net을 입력해주세요.")

                # 그래도 10초 대기
                time.sleep(10)

                screenshot_path = "C:\\appium\\manual_input_screenshot.png"
                driver.save_screenshot(screenshot_path)
                print(f"\n✓ 스크린샷 저장: {screenshot_path}")

        except Exception as e:
            print(f"\n⚠ URL 입력 중 오류: {str(e)}")

            screenshot_path = "C:\\appium\\error_screenshot.png"
            driver.save_screenshot(screenshot_path)
            print(f"\n✓ 오류 스크린샷 저장: {screenshot_path}")

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
    print("  Daum 접속 테스트 (Native App 방식)")
    print("=" * 60)
    print("\n")

    try:
        test_daum_with_native_browser()
        print("\n✓ 테스트 완료!")

    except KeyboardInterrupt:
        print("\n\n⚠ 사용자에 의해 테스트가 중단되었습니다.")
    except Exception as e:
        print(f"\n\n❌ 테스트 실패: {str(e)}")
        print("\n해결 방법:")
        print("1. Appium 서버가 http://localhost:4723 에서 실행 중인지 확인")
        print("2. Android 디바이스/에뮬레이터가 연결되어 있는지 확인 (adb devices)")
        print("3. Chrome 앱이 디바이스에 설치되어 있는지 확인")
