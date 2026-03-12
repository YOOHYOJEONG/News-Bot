# News Bot

네이버 뉴스 섹션에서 주요 기사 헤드라인을 수집해 보여주는 FastAPI 기반 뉴스 뷰어입니다.  
각 카테고리별로 상위 5개의 기사 제목과 원문 링크를 가져와 웹 화면에 표시합니다.

## 주요 기능

- 네이버 뉴스 섹션별 헤드라인 기사 크롤링
- 카테고리별 상위 5개 뉴스 제목 + 링크 제공
- `FastAPI` API와 간단한 프런트엔드 UI 제공
- 새로고침 버튼으로 최신 뉴스 다시 불러오기
- 현재 날짜, 요일, 마지막 불러온 시간 표시

## 크롤링 대상

현재 아래 네이버 뉴스 섹션을 대상으로 동작합니다.

- 금융: `https://news.naver.com/breakingnews/section/101/259`
- 부동산: `https://news.naver.com/breakingnews/section/101/260`
- 경제: `https://news.naver.com/breakingnews/section/101/262`
- 정치: `https://news.naver.com/section/100`
- 사회: `https://news.naver.com/section/102`
- IT/과학: `https://news.naver.com/section/105`
- 세계: `https://news.naver.com/section/104`

## 기술 스택

- Python 3.11
- FastAPI
- Jinja2
- Requests
- BeautifulSoup4
- Vanilla JavaScript
- CSS

## 프로젝트 구조

```text
news-bot/
├── crawler.py
├── main.py
├── requirements.txt
├── templates/
│   └── index.html
└── static/
    ├── app.js
    └── style.css
```

## 파일 설명

### `main.py`

- FastAPI 앱 엔트리 포인트입니다.
- `/` 경로에서 메인 페이지를 렌더링합니다.
- `/api/news` 경로에서 크롤링 결과를 JSON으로 반환합니다.

### `crawler.py`

- 네이버 뉴스 섹션별 크롤링 로직이 들어 있습니다.
- 각 URL별로 다른 CSS selector를 적용해 기사 제목과 링크를 추출합니다.
- 섹션별 결과를 `{카테고리명: [기사목록]}` 형식으로 반환합니다.

### `templates/index.html`

- 메인 화면의 기본 구조를 담당합니다.
- 제목, 날짜/시간 표시 영역, 새 뉴스 불러오기 버튼, 뉴스 목록 영역이 있습니다.

### `static/app.js`

- `/api/news`를 호출해 뉴스를 가져옵니다.
- 카테고리별 뉴스 목록을 동적으로 렌더링합니다.
- 페이지 진입 시 자동 로드 및 새로고침 버튼 동작을 담당합니다.
- 현재 날짜/요일/불러온 시간 표시를 갱신합니다.

### `static/style.css`

- 전체 UI 스타일을 담당합니다.
- 카테고리별 블록과 기사 리스트를 밝고 깔끔한 리스트형 레이아웃으로 구성합니다.

## 설치 방법

가상환경을 만든 뒤 의존성을 설치합니다.

```bash
pip install -r requirements.txt
```

## 실행 방법

개발 서버 실행:

```bash
uvicorn main:app --reload
```

브라우저에서 아래 주소로 접속합니다.

```text
http://localhost:8000
```

API 응답만 직접 확인하려면:

```text
http://localhost:8000/api/news
```

## API 예시

`GET /api/news`

예시 응답:

```json
{
  "금융": [
    {
      "title": "기사 제목",
      "link": "https://n.news.naver.com/..."
    }
  ],
  "정치": [
    {
      "title": "기사 제목",
      "link": "https://n.news.naver.com/..."
    }
  ]
}
```

## 동작 방식

1. 브라우저가 `/api/news`를 호출합니다.
2. 서버는 `crawler.py`에서 각 네이버 뉴스 섹션 HTML을 요청합니다.
3. 섹션별 selector로 기사 제목과 링크를 최대 5개까지 추출합니다.
4. JSON 응답을 프런트에서 받아 카테고리별 리스트 형태로 화면에 출력합니다.

## 참고 사항

- 네이버 뉴스 페이지 구조가 바뀌면 selector 수정이 필요할 수 있습니다.
- 일부 섹션은 `breakingnews` 계열, 일부는 `section` 계열이라 selector가 다르게 적용됩니다.
- 네트워크 상태나 사이트 응답 상태에 따라 특정 카테고리가 비어 있을 수 있습니다.


