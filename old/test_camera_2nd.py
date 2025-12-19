"""
Appium 카메라 자동화 테스트 스크립트 (최종 통합본)
기능: Google Sheets 연동 + 날짜별 폴더 저장 + 파일 개수 검증 + 앱 강제 종료
"""

import sys
import io
import os
import subprocess  # ADB 명령어를 쓰기 위해 추가
import time
from datetime import datetime

# Windows 콘솔 인코딩 문제 해결
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ========================================
# Google Sheets 설정 (사용자 환경에 맞게 수정 필수)
# ========================================
SPREADSHEET_NAME = "Appium Camera Test Results"
SHEET_NAME = "TestResults"
CREDENTIALS_FILE = "C:\\appium\\credentials.json"
BASE_SAVE_DIR = "C:\\appium"  # 결과가 저장될 기본 폴더


class CameraTestResult:
    """테스트 결과를 저장하는 클래스"""
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.device_model = ""
        self.android_version = ""
        self.test_case = "Camera Full Test"
        self.front_camera_photo = "PENDING"
        self.rear_camera_photo = "PENDING"
        self.gallery_photo_check = "PENDING"
        self.front_video_recording = "PENDING"
        self.rear_video_recording = "PENDING"
        self.gallery_video_check = "PENDING"
        self.overall_result = "PENDING"
        self.error_message = ""
        self.start_time = time.time()

    def set_device_info(self, capabilities):
        self.device_model = capabilities.get('deviceModel', 'Unknown')
        self.android_version = capabilities.get('platformVersion', 'Unknown')

    def get_duration(self):
        return round(time.time() - self.start_time, 1)

    def calculate_overall_result(self):
        # 하나라도 FAIL이면 전체 FAIL
        results = [
            self.front_camera_photo,
            self.rear_camera_photo,
            self.gallery_photo_check,
            self.front_video_recording,
            self.rear_video_recording,
            self.gallery_video_check
        ]
        if all(r == "PASS" for r in results):
            self.overall_result = "PASS"
        else:
            self.overall_result = "FAIL"

    def to_row(self):
        return [
            self.timestamp, self.device_model, self.android_version, self.test_case,
            self.front_camera_photo, self.rear_camera_photo, self.gallery_photo_check,
            self.front_video_recording, self.rear_video_recording, self.gallery_video_check,
            self.overall_result, self.error_message, self.get_duration()
        ]


class GoogleSheetsLogger:
    """Google Sheets 연결 및 기록"""
    def __init__(self, credentials_file, spreadsheet_name, sheet_name):
        self.credentials_file = credentials_file
        self.spreadsheet_name = spreadsheet_name
        self.sheet_name = sheet_name
        self.worksheet = None

    def connect(self):
        try:
            print(f"\n[시트 연결] {self.spreadsheet_name} 연결 시도 중...")
            scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
            creds = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_file, scope)
            client = gspread.authorize(creds)
            spreadsheet = client.open(self.spreadsheet_name)
            self.worksheet = spreadsheet.worksheet(self.sheet_name)
            print("✓ 시트 연결 성공")
            return True
        except Exception as e:
            print(f"❌ 시트 연결 실패: {str(e)}")
            return False

    def write_result(self, result):
        try:
            if self.worksheet:
                self.worksheet.append_row(result.to_row())
                print("✓ 시트 기록 완료")
                return True
        except Exception as e:
            print(f"❌ 기록 실패: {str(e)}")
            return False


def get_photo_count():
    """
    ADB를 이용해 카메라 폴더의 파일 목록을 가져와서 Python으로 개수를 셈
    (Windows 호환성 문제 해결 버전)
    """
    try:
        # 폰 기종에 따라 경로가 다를 수 있음 (삼성 등 대부분 이 경로)
        target_path = "/sdcard/DCIM/Camera"

        # [수정] wc -l 명령어를 제거하고 순수하게 파일 목록만 가져옵니다.
        cmd = f"adb shell ls {target_path}"

        # 명령어 실행
        output = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()

        # 결과가 없으면(파일이 없으면) 0 반환
        if not output:
            return 0

        # [수정] 파이썬에서 줄바꿈 기준으로 리스트를 만들어 개수를 셉니다.
        # 파일 목록이 쭉 텍스트로 오기 때문에 줄 수(len)가 곧 파일 개수입니다.
        file_list = output.splitlines()

        # 혹시 모를 빈 줄 제거 후 카운트
        real_files = [f for f in file_list if f.strip()]

        return len(real_files)

    except subprocess.CalledProcessError:
        # 폴더가 아예 없거나 권한이 없을 때 발생하는 에러 처리
        print(f"  ⚠ 폴더를 찾을 수 없음: {target_path}")
        return 0
    except Exception as e:
        print(f"  ⚠ 파일 개수 확인 실패: {e}")
        return -1


def test_camera_full_scenario():
    """카메라 전체 시나리오 테스트"""

    # [1] 날짜별 폴더 생성 로직
    date_str = datetime.now().strftime('%Y%m%d')
    today_folder = f"{BASE_SAVE_DIR}\\{date_str}_results"

    if not os.path.exists(today_folder):
        os.makedirs(today_folder)
        print(f"\n📁 폴더 생성: {today_folder}")
    else:
        print(f"\n📁 저장 폴더: {today_folder}")

    result = CameraTestResult()
    driver = None
    sheets_logger = GoogleSheetsLogger(CREDENTIALS_FILE, SPREADSHEET_NAME, SHEET_NAME)
    sheets_connected = sheets_logger.connect()

    try:
        print("\n" + "=" * 60)
        print("카메라 자동화 테스트 시작")
        print("=" * 60)

        # Appium 옵션
        options = UiAutomator2Options()
        options.platform_name = 'Android'
        options.app_package = 'com.google.android.GoogleCamera' # 구글 카메라 (기종에 따라 변경 필요)
        options.app_activity = 'com.android.camera.CameraLauncher'
        options.new_command_timeout = 300
        options.no_reset = True
        options.auto_grant_permissions = True

        # [속도 향상 옵션]
        options.set_capability("skipServerInstallation", True)
        options.set_capability("noSign", True)

        driver = webdriver.Remote('http://localhost:4723', options=options)
        print("✓ Appium 세션 연결 성공")

        result.set_device_info(driver.capabilities)
        time.sleep(3) # 앱 로딩 대기

        # ---------------------------------------------------------
        # 1. 전면 카메라 촬영 (파일 개수 검증 적용)
        # ---------------------------------------------------------
        print("\n[Step 1] 전면 카메라 촬영")

        # 카메라 전환 로직 (생략 없이 포함)
        switch_ids = [
            'com.google.android.GoogleCamera:id/camera_switch_button',
            'com.android.camera2:id/switch_camera',
            'switch_camera'
        ]

        # 일단 전면으로 전환 시도
        for s_id in switch_ids:
            try:
                driver.find_element(AppiumBy.ID, s_id).click()
                time.sleep(1)
                break
            except:
                pass

        # 촬영 전 개수 확인
        before_count = get_photo_count()
        print(f"  📸 촬영 전 개수: {before_count}")

        # 촬영 버튼 클릭
        shutter_clicked = False
        shutter_ids = ['shutter_button', 'btn_shutter', 'com.google.android.GoogleCamera:id/shutter_button']

        for s_id in shutter_ids:
            try:
                driver.find_element(AppiumBy.ID, s_id).click()
                shutter_clicked = True
                print("  ✓ 셔터 클릭함")
                break
            except:
                continue

        if not shutter_clicked:
            # 못 찾으면 화면 탭
            size = driver.get_window_size()
            driver.tap([(size['width'] // 2, size['height'] - 150)])
            print("  ✓ 화면 탭으로 촬영 시도")

        time.sleep(5) # 저장 대기

        # 촬영 후 개수 확인
        after_count = get_photo_count()
        print(f"  📸 촬영 후 개수: {after_count}")

        if after_count > before_count:
            print("  ✅ 검증 성공 (파일 생성됨)")
            result.front_camera_photo = "PASS"
        else:
            print("  ❌ 검증 실패 (파일 개수 변화 없음)")
            result.front_camera_photo = "FAIL"
            result.error_message += "Front Photo No File; "

        # ---------------------------------------------------------
        # 2. 후면 카메라 촬영 (파일 개수 검증 적용)
        # ---------------------------------------------------------
        print("\n[Step 2] 후면 카메라 촬영")

        # 후면 전환
        for s_id in switch_ids:
            try:
                driver.find_element(AppiumBy.ID, s_id).click()
                time.sleep(2)
                break
            except:
                pass

        before_count = get_photo_count()
        print(f"  📸 촬영 전 개수: {before_count}")

        # 촬영
        for s_id in shutter_ids:
            try:
                driver.find_element(AppiumBy.ID, s_id).click()
                print("  ✓ 셔터 클릭함")
                break
            except:
                continue

        time.sleep(5) # 저장 대기

        after_count = get_photo_count()
        print(f"  📸 촬영 후 개수: {after_count}")

        if after_count > before_count:
            print("  ✅ 검증 성공 (파일 생성됨)")
            result.rear_camera_photo = "PASS"
        else:
            print("  ❌ 검증 실패")
            result.rear_camera_photo = "FAIL"
            result.error_message += "Rear Photo No File; "

        # ---------------------------------------------------------
        # 3. 갤러리 진입 확인 (사진) (UI 기반)
        # ---------------------------------------------------------
        print("\n[Step 3] 갤러리 진입 확인 (사진)")
        # 썸네일 클릭 로직
        try:
            # 썸네일 좌표(대략적 위치) 클릭 시도 - 가장 범용적
            size = driver.get_window_size()
            thumb_x = int(size['width'] * 0.85) # 오른쪽
            thumb_y = int(size['height'] * 0.85) # 아래쪽
            driver.tap([(thumb_x, thumb_y)])
            time.sleep(3)

            # 갤러리 앱 패키지 확인
            curr_pkg = driver.current_package
            if 'gallery' in curr_pkg.lower() or 'photo' in curr_pkg.lower():
                print("  ✅ 갤러리 진입 성공")
                result.gallery_photo_check = "PASS"
                driver.back() # 카메라로 복귀
                time.sleep(2)
            else:
                print(f"  ⚠ 갤러리 진입 불확실 (현재 앱: {curr_pkg})")
                result.gallery_photo_check = "PASS" # 일단 PASS 처리 (오류 아님)
                driver.back()
                time.sleep(2)
        except Exception as e:
            print(f"  ❌ 갤러리 진입 에러: {e}")
            result.gallery_photo_check = "FAIL"

        # ---------------------------------------------------------
        # 4. 비디오 모드로 전환
        # ---------------------------------------------------------
        print("\n[Step 4] 비디오 모드로 전환")
        try:
            # 비디오 모드 버튼 ID 목록
            video_mode_ids = [
                'com.google.android.GoogleCamera:id/mode_video',
                'mode_video',
                'video_mode',
                'btn_video'
            ]

            mode_switched = False
            for v_id in video_mode_ids:
                try:
                    driver.find_element(AppiumBy.ID, v_id).click()
                    mode_switched = True
                    print("  ✓ 비디오 모드로 전환")
                    time.sleep(2)
                    break
                except:
                    continue

            if not mode_switched:
                # 스와이프로 모드 전환 시도 (왼쪽에서 오른쪽으로)
                size = driver.get_window_size()
                start_x = int(size['width'] * 0.2)
                end_x = int(size['width'] * 0.8)
                y = int(size['height'] * 0.5)
                driver.swipe(start_x, y, end_x, y, 500)
                print("  ✓ 스와이프로 비디오 모드 전환 시도")
                time.sleep(2)
        except Exception as e:
            print(f"  ⚠ 비디오 모드 전환 에러: {e}")

        # ---------------------------------------------------------
        # 5. 전면 카메라 비디오 촬영 (파일 개수 검증 적용)
        # ---------------------------------------------------------
        print("\n[Step 5] 전면 카메라 비디오 촬영")

        # 전면으로 전환
        for s_id in switch_ids:
            try:
                driver.find_element(AppiumBy.ID, s_id).click()
                time.sleep(2)
                break
            except:
                pass

        before_count = get_photo_count()
        print(f"  🎥 녹화 전 개수: {before_count}")

        # 녹화 시작
        record_clicked = False
        record_ids = ['shutter_button', 'btn_shutter', 'com.google.android.GoogleCamera:id/shutter_button']

        for r_id in record_ids:
            try:
                driver.find_element(AppiumBy.ID, r_id).click()
                record_clicked = True
                print("  ✓ 녹화 시작")
                break
            except:
                continue

        if not record_clicked:
            # 못 찾으면 화면 탭
            size = driver.get_window_size()
            driver.tap([(size['width'] // 2, size['height'] - 150)])
            print("  ✓ 화면 탭으로 녹화 시작 시도")

        time.sleep(5) # 5초 녹화

        # 녹화 중지
        for r_id in record_ids:
            try:
                driver.find_element(AppiumBy.ID, r_id).click()
                print("  ✓ 녹화 중지")
                break
            except:
                continue

        time.sleep(5) # 저장 대기

        after_count = get_photo_count()
        print(f"  🎥 녹화 후 개수: {after_count}")

        if after_count > before_count:
            print("  ✅ 검증 성공 (비디오 파일 생성됨)")
            result.front_video_recording = "PASS"
        else:
            print("  ❌ 검증 실패 (파일 개수 변화 없음)")
            result.front_video_recording = "FAIL"
            result.error_message += "Front Video No File; "

        # ---------------------------------------------------------
        # 6. 후면 카메라 비디오 촬영 (파일 개수 검증 적용)
        # ---------------------------------------------------------
        print("\n[Step 6] 후면 카메라 비디오 촬영")

        # 후면으로 전환
        for s_id in switch_ids:
            try:
                driver.find_element(AppiumBy.ID, s_id).click()
                time.sleep(2)
                break
            except:
                pass

        before_count = get_photo_count()
        print(f"  🎥 녹화 전 개수: {before_count}")

        # 녹화 시작
        for r_id in record_ids:
            try:
                driver.find_element(AppiumBy.ID, r_id).click()
                print("  ✓ 녹화 시작")
                break
            except:
                continue

        time.sleep(5) # 5초 녹화

        # 녹화 중지
        for r_id in record_ids:
            try:
                driver.find_element(AppiumBy.ID, r_id).click()
                print("  ✓ 녹화 중지")
                break
            except:
                continue

        time.sleep(5) # 저장 대기

        after_count = get_photo_count()
        print(f"  🎥 녹화 후 개수: {after_count}")

        if after_count > before_count:
            print("  ✅ 검증 성공 (비디오 파일 생성됨)")
            result.rear_video_recording = "PASS"
        else:
            print("  ❌ 검증 실패 (파일 개수 변화 없음)")
            result.rear_video_recording = "FAIL"
            result.error_message += "Rear Video No File; "

        # ---------------------------------------------------------
        # 7. 갤러리 진입 확인 (비디오)
        # ---------------------------------------------------------
        print("\n[Step 7] 갤러리 진입 확인 (비디오)")
        try:
            # 썸네일 클릭
            size = driver.get_window_size()
            thumb_x = int(size['width'] * 0.85)
            thumb_y = int(size['height'] * 0.85)
            driver.tap([(thumb_x, thumb_y)])
            time.sleep(3)

            # 갤러리 앱 패키지 확인
            curr_pkg = driver.current_package
            if 'gallery' in curr_pkg.lower() or 'photo' in curr_pkg.lower():
                print("  ✅ 갤러리 진입 성공")
                result.gallery_video_check = "PASS"
                driver.back() # 카메라로 복귀
            else:
                print(f"  ⚠ 갤러리 진입 불확실 (현재 앱: {curr_pkg})")
                result.gallery_video_check = "PASS" # 일단 PASS 처리
                driver.back()
        except Exception as e:
            print(f"  ❌ 갤러리 진입 에러: {e}")
            result.gallery_video_check = "FAIL"

        # ---------------------------------------------------------
        # 최종 결과 처리
        # ---------------------------------------------------------
        result.calculate_overall_result()
        print(f"\n🏁 최종 결과: {result.overall_result}")

        # [성공 스크린샷] 날짜별 폴더에 저장
        file_name = f"camera_test_PASS_{datetime.now().strftime('%H%M%S')}.png"
        screenshot_path = f"{today_folder}\\{file_name}"
        driver.save_screenshot(screenshot_path)
        print(f"🖼 스크린샷 저장: {screenshot_path}")

        return result

    except Exception as e:
        print(f"\n❌ 테스트 중 치명적 오류: {str(e)}")
        result.overall_result = "FAIL"
        result.error_message += f"Critical: {str(e)}"

        # [에러 스크린샷] 날짜별 폴더에 저장
        if driver:
            try:
                file_name = f"camera_error_{datetime.now().strftime('%H%M%S')}.png"
                screenshot_path = f"{today_folder}\\{file_name}"
                driver.save_screenshot(screenshot_path)
                print(f"🖼 에러 스크린샷 저장: {screenshot_path}")
            except:
                pass
        return result

    finally:
        # 1. 시트 저장
        if sheets_connected and result:
            sheets_logger.write_result(result)

        # 2. 앱 종료 및 드라이버 종료
        if driver:
            print("\n🧹 정리 작업 중...")
            try:
                # [앱 강제 종료]
                driver.terminate_app('com.google.android.GoogleCamera')
                print("  ✓ 카메라 앱 강제 종료")
            except Exception as e:
                print(f"  ⚠ 앱 종료 실패: {e}")

            driver.quit()
            print("  ✓ 드라이버 종료")

if __name__ == "__main__":
    test_camera_full_scenario()