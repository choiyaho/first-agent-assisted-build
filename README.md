# calffeine

> 소규모 카페 사장님이 메뉴 가격을 정할 때 쓰는 웹 애플리케이션 입니다.<br>
판매가·1잔 원가·예상 판매량·월 고정비를 넣어서 메뉴별 마진, 가게 전체 손익분기, 가격·판매량 시나리오 비교를 확인합니다.<br> 

<br>
<br>

## 디렉토리 구조

```
first-agent-assisted-build/
├── src/
│   ├── app.py              # 화면: 대시보드, 메뉴 카드, 시나리오. 계산은 calc.py를 부른다
│   ├── calc.py             # 계산 함수만. Streamlit을 쓰지 않아 따로 검사할 수 있다
│   ├── check_calc.py       # SPEC 손 계산 사례와 calc.py 결과를 대조 → check ok
│   ├── menu.csv            # 가상 예시 메뉴 12개와 메뉴별 그림 파일 이름
│   └── images/             # 메뉴 그림 SVG 13개 (새 메뉴용 기본 컵 포함)
├── docs/
│   ├── SPEC.md             # 정의 결정, 범위, 완료 기준, 손 계산 사례
│   ├── PLAN.md             # 단계표, 단계별 진행 기록, 바뀐 결정
│   └── cafe-pricing-plan.md  # 처음 구상 문서
├── .streamlit/config.toml  # 화면 테마 (글꼴, 색)
├── CLAUDE.md               # Claude Code 작업 규칙
├── requirements.txt        # streamlit==1.66.0
└── README.md
```

<br>
<br>

## 구현 방식

| 구분 | 사용한 것 |
|---|---|
| 언어 | Python 3.12 |
| 프론트엔드 | Streamlit 1.66 |
| 배포 | Streamlit Community Cloud. Github Repo를 연결하여, main에 push로 지속적 배포 가능 |
| 에이전트 | VS Code & Claude Code, CLAUDE.md에 작업 규칙, SPEC.md에 정의 결정과 손 계산 사례, PLAN.md에 단계와 결정 변경을 두고 한 단계씩 진행했다 |
| 스킬 | frontend-design 스킬(UI 개편과 검토), superpowers(SPEC.md & PLAN.md) 작성 |

계산(`calc.py`)과 화면(`app.py`)을 나눠, 계산은 Streamlit 없이 `check_calc.py`로 검사한다. 외부 API와 저장 기능은 쓰지 않는다.

<br>
<br>


## How to run / use

> 배포 앱<br>

https://calffeine.streamlit.app<br>
한동안 접속이 없으면 앱이 잠듭니다. 처음 열 때 깨우기 버튼이 보이면 눌러주시면 잠시 뒤에 실행됩니다.<br>

<br>
> 로컬 실행 (Python 3.12)

```sh
git clone https://github.com/choiyaho/first-agent-assisted-build.git
cd first-agent-assisted-build
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run src/app.py        # 브라우저가 http://localhost:8501 로 열린다
python src/check_calc.py        # 계산 검사 → "check ok"
```

<br>
<br>

## 사용 순서
```
1. 왼쪽 사이드바에 월 고정비(1원 이상)와 카드 수수료율(%)을 넣는다.
```
```
2. 메뉴명, 판매가, 한잔 원가 등 메뉴판 카드들의 내용을 매장에 맞게 적용한다. 최초 실행 시 가상 예시 메뉴 12개가 들어 있다. 없는 메뉴는 [삭제], 새 메뉴는 [+ 메뉴]로 추가한다.
```
```
3. 메인화면 상단 대시보드 우측의 [월 판매 계획]에서 메뉴별 예상 월 판매량을 고친다.
```
```
4. 메인 화면의 상단 대시보드에서 데이터들을 확인한다.
```
```
5. 「시나리오 비교」 탭에서 "가격을 바꾸면 한 달에 얼마나 남을까?"를 따져 본다.
```

- 입력한 값은 저장되지 않는다. 새로고침하면 예시 메뉴로 돌아간다.
<br>

### 용어
`1잔 이익` = 판매가÷1.1 − 원가 − 수수료.<br>
`원가율` = (원가+수수료)÷판매가.<br>
`마진율` = 1잔 이익÷판매가.<br>
`고정비 회수율` = 메뉴를 팔아 남긴 돈÷월 고정비(100% 이상이면 흑자).





