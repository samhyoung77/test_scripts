# Google Sheets 설정 상세 가이드

## 📝 스프레드시트 생성 및 설정

### 1단계: 새 스프레드시트 만들기

1. [Google Sheets](https://sheets.google.com) 접속
2. 좌측 상단 **+ 새로 만들기** 클릭 또는 빈 스프레드시트 클릭
3. 새 시트가 생성됩니다

---

### 2단계: 스프레드시트 이름 변경

1. 좌측 상단 **"제목 없는 스프레드시트"** 클릭
2. 이름 입력: `Appium Camera Test Results`
3. Enter 키 또는 다른 곳 클릭하면 자동 저장

![스프레드시트 이름 변경](https://i.imgur.com/example1.png)

**⚠️ 중요**: 이 이름을 나중에 Python 스크립트에서 사용합니다!

---

### 3단계: 시트 이름 변경

1. 하단의 **"시트1"** 탭 우클릭
2. **"이름 바꾸기"** 선택
3. 이름 입력: `TestResults`
4. Enter 키

또는:
- "시트1" 탭을 더블클릭해서 바로 수정

**⚠️ 중요**: 이 시트 이름도 Python 스크립트에서 사용합니다!

---

### 4단계: 헤더 행 설정

#### 방법 1: 수동 입력 (추천)

**A1 셀부터 M1 셀까지 다음 내용을 입력하세요:**

| 셀 | 입력 내용 |
|---|---|
| A1 | `Timestamp` |
| B1 | `Device Model` |
| C1 | `Android Version` |
| D1 | `Test Case` |
| E1 | `Front Camera Photo` |
| F1 | `Rear Camera Photo` |
| G1 | `Gallery Photo Check` |
| H1 | `Front Video Recording` |
| I1 | `Rear Video Recording` |
| J1 | `Gallery Video Check` |
| K1 | `Overall Result` |
| L1 | `Error Message` |
| M1 | `Duration (sec)` |

#### 방법 2: 복사 붙여넣기

아래 텍스트를 복사한 후, **A1 셀**에 붙여넣기:

```
Timestamp	Device Model	Android Version	Test Case	Front Camera Photo	Rear Camera Photo	Gallery Photo Check	Front Video Recording	Rear Video Recording	Gallery Video Check	Overall Result	Error Message	Duration (sec)
```

**📌 주의**: 각 항목 사이는 **탭(Tab)** 문자로 구분되어 있어야 자동으로 여러 셀로 분리됩니다.

---

### 5단계: 헤더 서식 꾸미기 (선택사항)

헤더를 눈에 띄게 만들려면:

1. **1행 전체** 선택 (행 번호 "1" 클릭)
2. 상단 도구 모음에서:
   - **굵게** (Ctrl+B)
   - **배경색** 선택 (연한 회색 또는 파란색 추천)
   - **텍스트 가운데 정렬**
3. 열 너비 자동 조정:
   - 모든 열 선택 (A~M)
   - 열 경계선 더블클릭 → 자동 맞춤

---

### 6단계: 서비스 계정과 공유

1. 우측 상단 **"공유"** 버튼 클릭
2. "사용자 및 그룹 추가" 입력란에 **서비스 계정 이메일** 입력

   📧 서비스 계정 이메일은 `credentials.json` 파일에서 확인:
   ```json
   {
     "client_email": "appium-test-bot@your-project-123456.iam.gserviceaccount.com"
   }
   ```

3. 권한 설정: **편집자** 선택
4. **"보내기"** 또는 **"공유"** 클릭

⚠️ **알림 보내기** 체크박스는 해제해도 됩니다 (봇 계정이므로)

---

### 7단계: 스프레드시트 URL 확인 (참고용)

공유가 완료되면 브라우저 주소창의 URL을 확인하세요:

```
https://docs.google.com/spreadsheets/d/1ABC...XYZ/edit#gid=0
```

이 URL에서:
- `1ABC...XYZ` 부분이 **스프레드시트 ID**입니다
- Python 스크립트는 이름으로 찾지만, ID로도 접근 가능합니다

---

## 📋 완성된 시트 예시

| Timestamp | Device Model | Android Version | Test Case | Front Camera Photo | Rear Camera Photo | Gallery Photo Check | Front Video Recording | Rear Video Recording | Gallery Video Check | Overall Result | Error Message | Duration (sec) |
|-----------|--------------|-----------------|-----------|-------------------|-------------------|---------------------|----------------------|---------------------|---------------------|----------------|---------------|----------------|
| 2025-01-15 14:30:25 | Pixel XL | 10 | Camera Full Test | PASS | PASS | PASS | PASS | PASS | PASS | PASS | - | 145.3 |
| 2025-01-15 15:20:10 | Pixel XL | 10 | Camera Full Test | PASS | FAIL | PASS | PASS | PASS | FAIL | FAIL | Rear camera: timeout | 132.8 |

**첫 번째 행(헤더)**만 직접 입력하세요. **두 번째 행부터**는 Python 스크립트가 자동으로 추가합니다!

---

## 🔧 Python 스크립트 설정

이제 `test_camera.py` 파일을 열고 다음 부분을 확인/수정하세요:

### 파일 위치: C:\appium\test_camera.py

**29~31번째 줄:**

```python
# Google Sheets 설정
SPREADSHEET_NAME = "Appium Camera Test Results"  # ← 4단계에서 설정한 이름
SHEET_NAME = "TestResults"                       # ← 5단계에서 설정한 시트 이름
CREDENTIALS_FILE = "C:\\appium\\credentials.json" # ← JSON 키 파일 경로
```

**⚠️ 주의사항:**
- 스프레드시트 이름과 시트 이름은 **대소문자 구분**됩니다
- 띄어쓰기도 정확히 일치해야 합니다
- 다른 이름을 사용했다면 반드시 이 부분을 수정하세요!

---

## ❓ FAQ

### Q1: 컬럼, 설명, 예시를 사전에 입력해야 하나요?

**아니요!** 다음만 입력하면 됩니다:

✅ **입력 필요**: 첫 번째 행(헤더)만
❌ **입력 불필요**: 예시 데이터 (2행부터)

Python 스크립트가 실행되면 자동으로 두 번째 행부터 데이터를 추가합니다.

### Q2: 헤더 행 순서를 바꾸고 싶어요

헤더 순서를 바꾸려면:

1. Google Sheets에서 열 순서 변경
2. Python 스크립트의 `to_row()` 메서드도 같이 수정

**예시: test_camera.py 220~234번째 줄**
```python
def to_row(self):
    """Google Sheets 행 데이터로 변환"""
    return [
        self.timestamp,           # A열
        self.device_model,        # B열
        self.android_version,     # C열
        # ... 순서 변경 시 여기도 수정
    ]
```

### Q3: 스프레드시트를 여러 개 만들고 싶어요

여러 테스트용 시트를 만들려면:

1. 각각 다른 이름으로 스프레드시트 생성
2. 스크립트 실행 시 `SPREADSHEET_NAME` 변수만 변경
3. 또는 명령줄 인자로 받도록 스크립트 수정

### Q4: 서비스 계정 이메일을 모르겠어요

`credentials.json` 파일을 텍스트 에디터로 열어서 확인:

```bash
notepad C:\appium\credentials.json
```

`"client_email"` 항목 찾기:
```json
{
  "type": "service_account",
  "project_id": "your-project-12345",
  "client_email": "appium-test-bot@your-project-12345.iam.gserviceaccount.com",
  ...
}
```

---

## ✅ 설정 완료 체크리스트

- [ ] Google Sheets 새로 만들기
- [ ] 스프레드시트 이름: "Appium Camera Test Results"로 변경
- [ ] 시트 이름: "TestResults"로 변경
- [ ] 첫 번째 행에 헤더 13개 입력 완료
- [ ] 서비스 계정 이메일과 공유 (편집자 권한)
- [ ] `test_camera.py` 파일의 설정 확인/수정
- [ ] `credentials.json` 파일이 `C:\appium\` 폴더에 있음

모두 완료하셨다면 테스트 실행 준비 완료! 🎉

---

## 🚀 테스트 실행

```bash
cd C:\appium
python test_camera.py
```

테스트가 완료되면 Google Sheets를 열어서 결과가 자동으로 추가되었는지 확인하세요!
