"""
Appium 테스트 스크립트 - Android Chrome으로 Daum 뉴스 크롤링
"""

import sys
import io

# Windows 콘솔 인코딩 문제 해결
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_daum_news():
    """Android Chrome에서 Daum 뉴스를 크롤링하는 테스트"""

    # Appium 옵션 설정
    options = UiAutomator2Options()
    options.platform_name = 'Android'
    options.automation_name = 'UiAutomator2'

    # Chrome 브라우저 사용 설정
    options.browser_name = 'Chrome'

    # Chromedriver 자동 다운로드 활성화 (Chrome 버전 자동 매칭)
    options.chromedriverAutodownload = True

    # Chromedriver 실행 가능 경로 자동 탐지
    options.chromedriverExecutableDir = 'C:\\Users\\siwoo\\.appium\\node_modules\\appium-uiautomator2-driver\\node_modules\\appium-chromedriver\\chromedrivers'

    # 선택사항: 특정 디바이스 지정 (adb devices로 확인한 디바이스명)
    # options.device_name = 'emulator-5554'  # 실제 디바이스명으로 변경
    options.device_name = 'Android'  # 자동 감지

    # 네트워크 속도 등을 고려한 타임아웃 설정
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

        # 암시적 대기 설정
        driver.implicitly_wait(10)

        print("\n" + "=" * 60)
        print("Daum 접속 중...")
        print("=" * 60)

        # Daum 접속
        driver.get('https://www.daum.net')
        time.sleep(3)  # 페이지 로딩 대기

        print("\n✓ Daum 메인 페이지 접속 성공!")
        print(f"✓ 현재 URL: {driver.current_url}")
        print(f"✓ 페이지 제목: {driver.title}")

        print("\n" + "=" * 60)
        print("주요 뉴스 정보 수집 중...")
        print("=" * 60)

        # 페이지가 완전히 로드될 때까지 대기
        wait = WebDriverWait(driver, 15)

        # 뉴스 목록 수집 (Daum 메인 페이지의 뉴스 섹션)
        news_list = []

        try:
            # Daum 메인의 뉴스 링크들 찾기 (여러 선택자 시도)
            selectors = [
                "//div[contains(@class, 'news')]//a[contains(@class, 'link')]",
                "//div[contains(@class, 'item_issue')]//a",
                "//ul[contains(@class, 'list_news')]//a",
                "//strong[@class='tit_g']//a",
                "//a[contains(@class, 'link_txt')]"
            ]

            news_elements = []
            for selector in selectors:
                try:
                    elements = driver.find_elements(By.XPATH, selector)
                    if elements and len(elements) > 0:
                        news_elements = elements[:10]  # 최대 10개
                        print(f"\n✓ 뉴스 요소 발견! (선택자: {selector[:50]}...)")
                        break
                except:
                    continue

            if not news_elements:
                # 모든 링크 가져오기 (대안)
                print("\n⚠ 특정 뉴스 선택자를 찾지 못했습니다. 모든 링크를 검색합니다...")
                all_links = driver.find_elements(By.TAG_NAME, "a")
                news_elements = [link for link in all_links if link.text.strip()][:10]

            print(f"\n✓ 총 {len(news_elements)}개의 뉴스 항목을 찾았습니다.\n")

            for idx, element in enumerate(news_elements, 1):
                try:
                    title = element.text.strip()
                    link = element.get_attribute('href')

                    if title and link:
                        news_item = {
                            'index': idx,
                            'title': title,
                            'url': link
                        }
                        news_list.append(news_item)

                        print(f"{idx}. {title}")
                        print(f"   URL: {link}")
                        print()

                except Exception as e:
                    continue

        except Exception as e:
            print(f"\n⚠ 뉴스 수집 중 오류: {str(e)}")
            print("\n페이지 소스 일부:")
            print(driver.page_source[:500])

        print("\n" + "=" * 60)
        print(f"수집 완료! 총 {len(news_list)}개의 뉴스 항목")
        print("=" * 60)

        # 스크린샷 저장
        screenshot_path = "C:\\appium\\daum_news_screenshot.png"
        driver.save_screenshot(screenshot_path)
        print(f"\n✓ 스크린샷 저장: {screenshot_path}")

        return news_list

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
    print("  Daum 뉴스 크롤링 테스트 (Appium + Android Chrome)")
    print("=" * 60)
    print("\n")

    try:
        news_data = test_daum_news()

        print("\n\n" + "=" * 60)
        print("최종 수집 결과")
        print("=" * 60)
        print(f"총 {len(news_data)}개의 뉴스 항목이 수집되었습니다.")

        if news_data:
            print("\n수집된 뉴스 목록:")
            for news in news_data:
                print(f"\n{news['index']}. {news['title']}")
                print(f"   {news['url']}")

    except KeyboardInterrupt:
        print("\n\n⚠ 사용자에 의해 테스트가 중단되었습니다.")
    except Exception as e:
        print(f"\n\n❌ 테스트 실패: {str(e)}")
        print("\n해결 방법:")
        print("1. Appium 서버가 http://localhost:4723 에서 실행 중인지 확인")
        print("2. Android 디바이스/에뮬레이터가 연결되어 있는지 확인 (adb devices)")
        print("3. Chrome 브라우저가 디바이스에 설치되어 있는지 확인")
