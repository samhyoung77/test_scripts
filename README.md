# 📸 Appium Android Camera Automation

Appium과 Python을 사용하여 안드로이드 디바이스의 카메라 기능을 자동으로 테스트하고, 결과를 Google Sheets에 기록하는 자동화 프로젝트입니다.

## 📋 주요 기능 (Features)
- **자동 촬영:** 전면/후면 카메라 사진 및 동영상 촬영 자동화
- **검증 로직:** ADB를 이용하여 실제 파일 생성 여부(File Count) 검증
- **결과 리포팅:** Google Sheets API를 통해 테스트 결과(PASS/FAIL) 및 소요시간 실시간 기록
- **대시보드:** Google Sheets Apps Script를 활용한 시각화 대시보드 제공
- **버전 관리:** 테스트 실행 시 코드 버전(Version) 정보 자동 기록

## 🛠️ 요구 사항 (Prerequisites)
- macOS 
- Python 3.x
- Appium Server & Inspector
- Android Device (Developer Mode ON, USB Debugging ON)
- Google Cloud Service Account (`credentials.json`) - 별도 파일복사 필요 

## 📦 설치 및 실행 (Installation & Usage)

1. **저장소 클론**
   ```bash
   git clone [https://github.com/samhyoung77/test_scripts.git](https://github.com/samhyoung77/test_scripts.git)
   cd test_scripts