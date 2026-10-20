# calffeine

소규모 카페 사장님이 메뉴 가격을 정할 때 쓰는 웹앱. 판매가·1잔 원가·예상 판매량·월 고정비를 넣으면 메뉴별 마진, 가게 전체 손익분기, 가격·판매량 시나리오 비교를 보여준다. 정의와 범위는 [docs/SPEC.md](docs/SPEC.md).

## How to run / use

> 초안 (Claude 작성). `src/app.py`는 PLAN 2단계에서 만든다.

```sh
git clone https://github.com/choiyaho/first-agent-assisted-build.git
cd first-agent-assisted-build
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run src/app.py        # 브라우저가 http://localhost:8501 로 열린다
python src/check_calc.py        # 계산 검사 → "check ok"
```

사용 순서
1. 왼쪽 사이드바에 월 고정비와 카드 수수료율(%)을 넣는다. 고정비에는 사장 본인 인건비도 포함하는 것을 권장한다.
2. 「메뉴와 마진」 탭의 표에서 메뉴명, 판매가(부가세 포함), 1잔 원가(재료+포장), 예상 월 판매량을 고친다. 행을 추가·삭제할 수 있다. 처음에는 가상 예시 메뉴가 들어 있다.
3. 메뉴별 1잔 이익·원가율·마진율과 위쪽 카드(월 이익, 손익분기 잔 수·매출액)를 확인한다. 팔수록 손해인 메뉴는 경고가 뜬다.
4. 「시나리오」 탭에서 A·B의 가격 변화(%)와 판매량 변화(%)를 조정해 현재와 월 이익을 비교한다.

용어: 1잔 이익 = 판매가÷1.1 − 원가 − 수수료. 원가율 = (원가+수수료)÷판매가. 마진율 = 1잔 이익÷판매가.

## Work process

## Claude Code evidence

## Three effective practices

## Three difficulties
