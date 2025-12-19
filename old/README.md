# Appium Android Chrome 테스트

Android 디바이스의 Chrome 브라우저로 Daum 뉴스를 크롤링하는 자동화 테스트입니다.

## 사전 준비

### 1. Appium 설치
```bash
npm install -g appium
```

### 2. Appium UiAutomator2 드라이버 설치
```bash
appium driver install uiautomator2
```

### 3. Python 패키지 설치
```bash
pip install Appium-Python-Client
```

### 4. Android SDK 및 ADB 설정
- Android Studio를 설치하거나
- ADB (Android Debug Bridge)가 시스템 PATH에 있어야 합니다

### 5. Android 디바이스 준비
- USB 디버깅 활성화
- Chrome 브라우저 설치 확인

## 테스트 실행 방법

### Step 1: Android 디바이스 연결 확인
```bash
adb devices
```

출력 예시:
```
List of devices attached
emulator-5554   device
```

### Step 2: Appium 서버 실행
새 터미널에서:
```bash
appium
```

출력 예시:
```
[Appium] Welcome to Appium v2.x.x
[Appium] Appium REST http interface listener started on http://0.0.0.0:4723
```

### Step 3: 테스트 스크립트 실행
다른 터미널에서:
```bash
cd C:\appium
python test_daum_news.py
```

## 스크립트 기능

- ✅ Android Chrome 브라우저 자동 실행
- ✅ Daum (www.daum.net) 메인 페이지 접속
- ✅ 주요 뉴스 제목 및 링크 수집 (최대 10개)
- ✅ 자동 스크린샷 저장
- ✅ 오류 발생 시 디버깅 정보 제공

## 출력 파일

- `daum_news_screenshot.png` - 정상 실행 시 스크린샷
- `error_screenshot.png` - 오류 발생 시 스크린샷

## 트러블슈팅

### 문제 1: "ModuleNotFoundError: No module named 'appium'"
**해결:**
```bash
pip install Appium-Python-Client
```

### 문제 2: "Could not connect to Appium server"
**해결:**
- Appium 서버가 실행 중인지 확인
```bash
appium
```

### 문제 3: "No devices found"
**해결:**
- Android 디바이스가 연결되었는지 확인
```bash
adb devices
```
- USB 디버깅이 활성화되었는지 확인

### 문제 4: "Chrome not found"
**해결:**
- 디바이스에 Chrome 브라우저 설치 확인
- Chrome WebDriver가 호환되는지 확인

### 문제 5: 뉴스를 찾지 못함
**해결:**
- Daum 웹사이트 구조가 변경되었을 수 있음
- 스크린샷 확인하여 페이지가 제대로 로드되었는지 확인
- 네트워크 연결 상태 확인

## 커스터마이징

### 특정 디바이스 지정
`test_daum_news.py` 파일에서:
```python
options.device_name = 'emulator-5554'  # 실제 디바이스명으로 변경
```

### 수집할 뉴스 개수 변경
```python
news_elements = elements[:10]  # 10을 원하는 숫자로 변경
```

### 다른 웹사이트로 변경
```python
driver.get('https://www.daum.net')  # URL 변경
```

## 참고 자료

- [Appium 공식 문서](https://appium.io/docs/en/latest/)
- [Appium Python Client](https://github.com/appium/python-client)
- [Selenium Python 문서](https://selenium-python.readthedocs.io/)
