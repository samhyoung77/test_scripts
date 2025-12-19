# Appium Inspector 사용 가이드

## 📥 1. Appium Inspector 다운로드

https://github.com/appium/appium-inspector/releases

최신 버전 다운로드 (Windows: `Appium-Inspector-windows-...exe`)

---

## ⚙️ 2. Capability 설정값

Appium Inspector를 실행한 후, 다음 값들을 입력하세요:

### Remote Host
```
localhost
```

### Remote Port
```
4723
```

### Remote Path
```
/
```

---

## 📋 3. Desired Capabilities (JSON 형식)

아래 JSON을 **JSON Representation** 탭에 복사/붙여넣기:

```json
{
  "platformName": "Android",
  "appium:automationName": "UiAutomator2",
  "appium:deviceName": "Android",
  "appium:appPackage": "com.google.android.GoogleCamera",
  "appium:appActivity": "com.android.camera.CameraLauncher",
  "appium:noReset": true,
  "appium:autoGrantPermissions": true,
  "appium:newCommandTimeout": 300
}
```

또는 **개별 입력 방식**:

| Key | Value |
|-----|-------|
| `platformName` | `Android` |
| `appium:automationName` | `UiAutomator2` |
| `appium:deviceName` | `Android` |
| `appium:appPackage` | `com.google.android.GoogleCamera` |
| `appium:appActivity` | `com.android.camera.CameraLauncher` |
| `appium:noReset` | `true` |
| `appium:autoGrantPermissions` | `true` |
| `appium:newCommandTimeout` | `300` |

---

## 🚀 4. 사용 방법

### Step 1: Appium 서버 시작

```bash
cd C:\appium
start_appium.bat
```

또는

```bash
set ANDROID_HOME=C:\Users\siwoo\AppData\Local\Android\Sdk
set ANDROID_SDK_ROOT=C:\Users\siwoo\AppData\Local\Android\Sdk
appium
```

### Step 2: Android 디바이스 연결 확인

```bash
adb devices
```

### Step 3: Appium Inspector 실행

1. Appium Inspector 앱 실행
2. 위의 Capability 값 입력
3. **"Start Session"** 클릭

### Step 4: UI 요소 찾기

**찾아야 할 요소:**

1. **썸네일 버튼** (우측 하단)
   - 마우스로 클릭하면 Inspector가 요소 정보 표시
   - `resource-id`, `content-desc`, `class`, `bounds` 확인

2. **셔터 버튼** (중앙 하단)
   - ID 확인

3. **카메라 전환 버튼**
   - ID 확인

4. **비디오 모드 전환 버튼**
   - ID 확인

---

## 🔍 5. 확인할 정보

각 버튼을 클릭하여 다음 정보를 확인:

### 썸네일 버튼
```
resource-id: ??? (이 값이 중요!)
content-desc: ???
class: ???
bounds: ???
clickable: true/false
```

### 셔터 버튼
```
resource-id: ???
content-desc: ???
```

### 카메라 전환 버튼
```
resource-id: ???
content-desc: ???
```

---

## 📝 6. 정보 수집 템플릿

발견한 정보를 다음 형식으로 알려주세요:

```
1. 썸네일 버튼
   - resource-id: com.google.android.GoogleCamera:id/xxxxx
   - content-desc: xxxxx
   - bounds: [x1,y1][x2,y2]

2. 셔터 버튼
   - resource-id: com.google.android.GoogleCamera:id/xxxxx
   - content-desc: xxxxx

3. 카메라 전환 버튼 (전면/후면)
   - resource-id: com.google.android.GoogleCamera:id/xxxxx
   - content-desc: xxxxx

4. 비디오 모드 버튼
   - resource-id: com.google.android.GoogleCamera:id/xxxxx
   - content-desc: xxxxx
```

---

## 💡 7. 스크린샷 캡처 방법

Appium Inspector에서:

1. 요소를 클릭하여 선택
2. 우측 패널에서 정보 확인
3. **"Copy XML"** 버튼으로 XML 복사 가능
4. 스크린샷 캡처 (Windows: Win+Shift+S)

---

## ⚠️ 8. 문제 해결

### "Could not start session" 에러

**원인**: Appium 서버가 실행 중이 아님

**해결**:
```bash
appium
```

### "An unknown server-side error occurred"

**원인**: 디바이스가 연결되지 않음

**해결**:
```bash
adb devices
adb kill-server
adb start-server
adb devices
```

### 카메라 앱이 열리지 않음

**해결**: 수동으로 카메라를 먼저 실행한 후, Inspector에서 다음 Capability 사용:

```json
{
  "platformName": "Android",
  "appium:automationName": "UiAutomator2",
  "appium:deviceName": "Android",
  "appium:noReset": true,
  "appium:autoGrantPermissions": true
}
```

(appPackage, appActivity 제거)

---

## 🎯 9. 다음 단계

UI 요소 정보를 확인한 후:

1. 이 문서에 기록
2. 정보를 알려주시면 스크립트 수정
3. 테스트 재실행

---

## 📸 10. 참고 이미지

Appium Inspector 화면:

```
┌─────────────────────────────────────────────┐
│  Appium Inspector                           │
├─────────────────────────────────────────────┤
│  ┌─────────────┐  ┌────────────────────┐   │
│  │             │  │ Element Details    │   │
│  │  Device     │  │                    │   │
│  │  Screen     │  │ resource-id:       │   │
│  │             │  │ content-desc:      │   │
│  │             │  │ class:             │   │
│  │   [📷]      │  │ bounds:            │   │
│  │             │  │ clickable: true    │   │
│  │             │  │                    │   │
│  │     👆       │  │ [Copy XML]         │   │
│  │  thumbnail  │  │                    │   │
│  └─────────────┘  └────────────────────┘   │
└─────────────────────────────────────────────┘
```

---

이 정보를 확인하면 스크립트를 정확하게 수정할 수 있습니다! 😊
