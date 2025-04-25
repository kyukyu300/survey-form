# 📋 심리테스트 검사 폼 만들기
**간단한 몇가지 질문을 통하여 성향 테스트를 할 수 있는 웹 애플리케이션입니다.**

## 📌 프로젝트 파일 구조
```bash
/
├── run.py             # 앱 실행 스크립트 (개발용)
├── wsgi.py            # WSGI 서버용 진입점
├── config.py          # 환경 설정 파일
├── app/               # 애플리케이션 패키지
│   ├── init.py        # Flask 앱 팩토리 및 초기화
│   ├── models.py      # 데이터베이스 모델 정의
│   ├── routes.py      # 라우팅 및 뷰 함수
│   └── services/      # 비즈니스 로직 모듈
│       ├── answers.py   # 답변 관련 서비스
│       ├── choices.py   # 선택지 관련 서비스
│       ├── images.py    # 이미지 처리 관련 서비스
│       ├── questions.py # 질문 관련 서비스
│       └── users.py     # 사용자 관련 서비스
```

## ⤵️ 설치 방법 
```bash
git clone https://github.com/kyukyu300/survey-form.git  # 프로젝트 파일 복제하기
cd survey-form                                          # 파일 위치로 이동
```

## ✴️ 가상환경 활성화
```bash
# 가상환경 생성
python -m venv .venv      
# 가상환경 활성화
source .venv/bin/activate   # mac / Linux
.venv\Scripts\activate      # Windows
```

## ⤵️ 의존성 설치
```bash
pip install -r requirements.txt
```
## ▶️ 실행 방법
```bash
python run.py  # 개발환경
python wsgi.py # 배포
```
## 실행 화면
추가 예정
