# 카메라 테스트 문제 해결 가이드

## 🔍 발견된 문제

1. **카메라 앱이 홈 화면으로 전환됨**
   - Appium 세션 시작 시 홈 화면으로 이동
   - 테스트 중간에 브라우저나 다른 앱이 열림

2. **썸네일 클릭 실패**
   - UI 요소를 찾지 못함
   - 좌표 기반 클릭도 정확하지 않음

---

## ✅ 해결 방법

### 방법 1: 옵션 추가 (권장)

test_camera.py의 177-183번째 줄을 다음과 같이 수정:

```python
# 카메라 앱 직접 지정 (가장 확실한 방법)
options.app_package = 'com.google.android.GoogleCamera'
options.app_activity = 'com.android.camera.CameraLauncher'

options.new_command_timeout = 300
options.no_reset = True
options.full_reset = False  # 추가
options.auto_grant_permissions = True
options.dont_stop_app_on_reset = True
options.skip_unlock = True  # 추가
options.skip_device_initialization = True  # 추가
```

### 방법 2: 각 단계마다 카메라 확인 추가

각 테스트 단계 시작 전에 다음 코드 추가:

```python
# 카메라 앱 확인 및 복귀
current_pkg = driver.current_package
if 'camera' not in current_pkg.lower():
    print(f"  ⚠ 다른 앱 감지: {current_pkg}, 카메라로 복귀...")
    driver.execute_script('mobile: startActivity', {
        'component': 'com.google.android.GoogleCamera/com.android.camera.CameraLauncher'
    })
    time.sleep(2)
```

### 방법 3: 썸네일 찾기 개선

실제 디바이스의 UI 요소를 확인한 결과, Google Camera는 다음 ID를 사용:

```python
# 실제로 작동하는 썸네일 ID (우선순위대로)
thumbnail_ids = [
    'com.google.android.GoogleCamera:id/filmstrip_view',  # 가장 확실
    'com.google.android.GoogleCamera:id/bottom_bar',
    'com.google.android.GoogleCamera:id/rounded_thumbnail_view',
]
```

---

## 🚀 빠른 테스트

간단한 버전으로 먼저 테스트:

```bash
cd C:\appium
python test_camera_simple.py
```

이 스크립트로 현재 화면의 모든 클릭 가능한 요소를 확인할 수 있습니다.

---

## 💡 추천 해결책

가장 안정적인 방법:

1. **수동 실행 방식 사용**
   - 스크립트는 디바이스만 연결
   - 사용자가 수동으로 카메라 실행
   - 스크립트가 UI 요소만 제어

2. **ADB 명령어로 직접 제어**
   - 카메라 실행: `adb shell am start -n com.google.android.GoogleCamera/com.android.camera.CameraLauncher`
   - Input 이벤트로 제어

---

## 🔧 최종 권장 사항

현재 스크립트가 복잡하므로, 더 간단하고 안정적인 버전을 만드는 것을 추천합니다:

1. **Step 1**: 디바이스 연결만
2. **Step 2**: ADB로 카메라 실행
3. **Step 3**: UI Automator로 요소 제어
4. **Step 4**: 스크린샷으로 결과 확인

이 방식이 더 안정적이고 디버깅하기 쉽습니다.
