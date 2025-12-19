# 카메라 자동화 테스트 설정 가이드

## 📋 1. 사전 준비 사항

### 1-1. Python 패키지 설치

```bash
pip install Appium-Python-Client
pip install gspread oauth2client
pip install pillow  # 이미지 분석용 (선택)
```

### 1-2. Google Sheets API 설정

#### Step 1: Google Cloud Console에서 프로젝트 생성

1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. 새 프로젝트 생성 (예: "Appium-Camera-Test")

#### Step 2: Google Sheets API 활성화

1. 좌측 메뉴 > "API 및 서비스" > "라이브러리"
2. "Google Sheets API" 검색
3. "사용 설정" 클릭
4. "Google Drive API"도 동일하게 활성화

#### Step 3: 서비스 계정 생성

1. 좌측 메뉴 > "API 및 서비스" > "사용자 인증 정보"
2. "사용자 인증 정보 만들기" > "서비스 계정" 선택
3. 서비스 계정 이름 입력 (예: "appium-test-bot")
4. "만들기 및 계속" 클릭
5. 역할: "편집자" 선택
6. "완료" 클릭

#### Step 4: JSON 키 파일 다운로드

1. 생성된 서비스 계정 클릭
2. "키" 탭 선택
3. "키 추가" > "새 키 만들기"
4. 키 유형: JSON 선택
5. "만들기" 클릭 → JSON 파일 자동 다운로드
6. 다운로드된 JSON 파일을 `C:\appium\credentials.json`으로 저장

#### Step 5: Google Sheets 생성 및 공유

1. [Google Sheets](https://sheets.google.com) 접속
2. 새 스프레드시트 만들기
3. 이름: "Appium Camera Test Results"
4. 우측 상단 "공유" 버튼 클릭
5. 서비스 계정 이메일 추가 (credentials.json 파일 안의 "client_email" 값)
   - 예: `appium-test-bot@your-project.iam.gserviceaccount.com`
6. 권한: "편집자"로 설정
7. "공유" 클릭

### 1-3. Android 디바이스 설정

1. **개발자 옵션 활성화**
   - 설정 > 휴대전화 정보 > 빌드 번호 7번 탭

2. **USB 디버깅 활성화**
   - 설정 > 개발자 옵션 > USB 디버깅 ON

3. **카메라 권한 허용**
   - 설정 > 앱 > 카메라 > 권한 > 모두 허용

4. **자동 화면 꺼짐 방지**
   - 설정 > 개발자 옵션 > 화면 항상 켜기 ON

### 1-4. Appium 환경 설정

```bash
# Android SDK 환경 변수 설정 (PowerShell)
$env:ANDROID_HOME="C:\Users\siwoo\AppData\Local\Android\Sdk"
$env:ANDROID_SDK_ROOT="C:\Users\siwoo\AppData\Local\Android\Sdk"

# Appium 서버 시작
appium --allow-insecure=uiautomator2:chromedriver_autodownload
```

---

## 📊 2. Google Sheets 구성

### 시트 이름: "TestResults"

| 컬럼 | 설명 | 예시 |
|------|------|------|
| A: Timestamp | 테스트 실행 시간 | 2025-01-15 14:30:25 |
| B: Device Model | 디바이스 모델 | Pixel XL |
| C: Android Version | Android 버전 | 10 |
| D: Test Case | 테스트 케이스 | Camera Full Test |
| E: Front Camera Photo | 전면 카메라 촬영 | PASS / FAIL |
| F: Rear Camera Photo | 후면 카메라 촬영 | PASS / FAIL |
| G: Gallery Photo Check | 갤러리 사진 확인 | PASS / FAIL |
| H: Front Video Recording | 전면 동영상 녹화 | PASS / FAIL |
| I: Rear Video Recording | 후면 동영상 녹화 | PASS / FAIL |
| J: Gallery Video Check | 갤러리 영상 확인 | PASS / FAIL |
| K: Overall Result | 전체 결과 | PASS / FAIL |
| L: Error Message | 에러 메시지 (있는 경우) | - |
| M: Duration (sec) | 테스트 소요 시간 | 85.3 |

### 헤더 설정 (첫 번째 행)

```
Timestamp | Device Model | Android Version | Test Case | Front Camera Photo | Rear Camera Photo | Gallery Photo Check | Front Video Recording | Rear Video Recording | Gallery Video Check | Overall Result | Error Message | Duration (sec)
```

---

## 📝 3. credentials.json 파일 위치

파일 경로: `C:\appium\credentials.json`

파일 형식:
```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "...",
  "private_key": "...",
  "client_email": "appium-test-bot@your-project.iam.gserviceaccount.com",
  "client_id": "...",
  ...
}
```

---

## 🔧 4. 테스트 스크립트 설정

테스트 스크립트 실행 전에 `test_camera.py` 파일에서 다음 정보를 수정하세요:

```python
# Google Sheets 설정
SPREADSHEET_NAME = "Appium Camera Test Results"  # 실제 스프레드시트 이름
SHEET_NAME = "TestResults"  # 시트 이름
CREDENTIALS_FILE = "C:\\appium\\credentials.json"  # JSON 키 파일 경로
```

---

## ✅ 5. 설정 확인 체크리스트

- [ ] Python 패키지 설치 완료 (`gspread`, `oauth2client`, `Appium-Python-Client`)
- [ ] Google Cloud Console에서 프로젝트 생성
- [ ] Google Sheets API 활성화
- [ ] Google Drive API 활성화
- [ ] 서비스 계정 생성 및 JSON 키 다운로드
- [ ] `credentials.json` 파일을 `C:\appium\` 폴더에 저장
- [ ] Google Sheets 생성 및 서비스 계정과 공유
- [ ] 스프레드시트에 헤더 행 작성
- [ ] Android 디바이스 USB 디버깅 활성화
- [ ] Android 디바이스 연결 확인 (`adb devices`)
- [ ] Appium 서버 실행 중
- [ ] 환경 변수 설정 (ANDROID_HOME, ANDROID_SDK_ROOT)

---

## 🚀 6. 테스트 실행

```bash
cd C:\appium
python test_camera.py
```

테스트가 성공하면 Google Sheets에 자동으로 결과가 기록됩니다!

---

## ⚠️ 문제 해결

### Google Sheets 접근 오류
- 서비스 계정 이메일이 스프레드시트에 공유되었는지 확인
- `credentials.json` 파일 경로가 올바른지 확인

### 카메라 앱 실행 실패
- 디바이스의 카메라 앱 패키지명 확인 필요
- 제조사별로 패키지명이 다를 수 있음

### 요소를 찾을 수 없음
- 디바이스 제조사/모델에 따라 UI 요소 ID가 다를 수 있음
- Appium Inspector로 실제 요소 확인 필요
