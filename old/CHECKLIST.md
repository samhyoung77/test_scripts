# 카메라 테스트 설정 체크리스트

> 각 항목을 완료하면 `[ ]`를 `[x]`로 변경하세요!

---

## 📦 1단계: Python 환경 설정

- [ ] Python 3.7 이상 설치 확인
  ```bash
  python --version
  ```

- [ ] 필요한 패키지 설치
  ```bash
  pip install -r C:\appium\requirements.txt
  ```

- [ ] 설치 확인
  ```bash
  pip list | findstr "Appium gspread oauth2client"
  ```

---

## ☁️ 2단계: Google Cloud Console 설정

- [ ] Google Cloud Console 접속
  - URL: https://console.cloud.google.com/

- [ ] 새 프로젝트 생성
  - 프로젝트 이름: `Appium-Camera-Test` (또는 원하는 이름)

- [ ] Google Sheets API 활성화
  - 좌측 메뉴 > API 및 서비스 > 라이브러리
  - "Google Sheets API" 검색 후 활성화

- [ ] Google Drive API 활성화
  - "Google Drive API" 검색 후 활성화

- [ ] 서비스 계정 생성
  - API 및 서비스 > 사용자 인증 정보
  - "사용자 인증 정보 만들기" > "서비스 계정"
  - 이름: `appium-test-bot`
  - 역할: "편집자"

- [ ] JSON 키 파일 다운로드
  - 서비스 계정 클릭 > 키 탭 > 키 추가 > JSON 선택
  - 다운로드된 파일을 `C:\appium\credentials.json`으로 저장

---

## 📊 3단계: Google Sheets 설정

- [ ] Google Sheets 접속
  - URL: https://sheets.google.com

- [ ] 새 스프레드시트 생성

- [ ] 스프레드시트 이름 변경
  - 이름: `Appium Camera Test Results`

- [ ] 시트 이름 변경
  - "시트1" → `TestResults`

- [ ] 헤더 행 입력 (A1~M1에 가로로)
  - A1: `Timestamp`
  - B1: `Device Model`
  - C1: `Android Version`
  - D1: `Test Case`
  - E1: `Front Camera Photo`
  - F1: `Rear Camera Photo`
  - G1: `Gallery Photo Check`
  - H1: `Front Video Recording`
  - I1: `Rear Video Recording`
  - J1: `Gallery Video Check`
  - K1: `Overall Result`
  - L1: `Error Message`
  - M1: `Duration (sec)`

- [ ] 서비스 계정과 공유
  - 우측 상단 "공유" 버튼
  - credentials.json의 `client_email` 주소 입력
  - 권한: "편집자"

---

## 📱 4단계: Android 디바이스 설정

- [ ] USB 디버깅 활성화
  - 설정 > 휴대전화 정보 > 빌드 번호 7번 탭
  - 설정 > 개발자 옵션 > USB 디버깅 ON

- [ ] 디바이스 연결 확인
  ```bash
  adb devices
  ```
  출력 예: `HT76M0204943    device`

- [ ] 카메라 권한 확인
  - 설정 > 앱 > 카메라 > 권한 > 모두 허용

- [ ] 화면 꺼짐 방지 설정
  - 설정 > 개발자 옵션 > 화면 항상 켜기 ON

---

## 🖥️ 5단계: Appium 환경 설정

- [ ] Appium 설치 확인
  ```bash
  appium --version
  ```

- [ ] UiAutomator2 드라이버 설치 확인
  ```bash
  appium driver list --installed
  ```

- [ ] Android SDK 경로 확인
  ```bash
  where adb
  ```
  출력: `C:\Users\siwoo\AppData\Local\Android\Sdk\platform-tools\adb.exe`

- [ ] 환경 변수 설정 (매번 Appium 실행 전에 필요)
  ```bash
  set ANDROID_HOME=C:\Users\siwoo\AppData\Local\Android\Sdk
  set ANDROID_SDK_ROOT=C:\Users\siwoo\AppData\Local\Android\Sdk
  ```

---

## 🔧 6단계: 테스트 스크립트 설정

- [ ] credentials.json 파일 위치 확인
  - 경로: `C:\appium\credentials.json`

- [ ] test_camera.py 설정 확인
  - 29번째 줄: `SPREADSHEET_NAME = "Appium Camera Test Results"`
  - 30번째 줄: `SHEET_NAME = "TestResults"`
  - 31번째 줄: `CREDENTIALS_FILE = "C:\\appium\\credentials.json"`

- [ ] 카메라 앱 패키지명 확인 (디바이스에 맞게 수정)
  - Google/Pixel: `com.android.camera2`
  - Samsung: `com.sec.android.app.camera`
  - LG: `com.lge.camera`

---

## 🎯 7단계: 테스트 실행 준비

- [ ] Appium 서버 시작
  ```bash
  appium
  ```

- [ ] 간단한 연결 테스트
  ```bash
  python C:\appium\test_simple.py
  ```

- [ ] 테스트 결과: PASS 확인

---

## ✅ 최종 확인

모든 항목이 체크되었다면 카메라 테스트를 실행할 준비가 완료되었습니다!

```bash
cd C:\appium
python test_camera.py
```

---

## 📝 메모

이 체크리스트를 인쇄하거나 별도로 저장해서 사용하세요.
완료한 항목은 `[x]`로 표시하면 진행 상황을 쉽게 파악할 수 있습니다!

**마지막 업데이트:** 2025-01-15
