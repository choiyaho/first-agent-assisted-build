# calffeine

소규모 카페 사장님이 메뉴 가격을 정할 때 쓰는 웹앱. 판매가·1잔 원가·예상 판매량·월 고정비를 넣으면 메뉴별 마진, 가게 전체 손익분기, 가격·판매량 시나리오 비교를 보여준다. 정의와 범위는 [docs/SPEC.md](docs/SPEC.md).

## How to run / use

> 초안 (Claude 작성).

배포 앱: https://calffeine.streamlit.app
한동안 접속이 없으면 앱이 잠듭니다. 처음 열 때 깨우기 버튼이 보이면 눌러 주세요. 잠시 뒤 실행됩니다.

로컬 실행 (Python 3.12)

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
1. 왼쪽 사이드바에 월 고정비(1원 이상)와 카드 수수료율(%)을 넣는다. 고정비에는 사장 본인 인건비도 포함하는 것을 권장한다.
2. 「메뉴판」의 카드에서 메뉴명, 판매가(부가세 포함), 1잔 원가(재료+포장)를 고친다. 처음에는 가상 예시 메뉴 12개가 들어 있다. 없는 메뉴는 [삭제], 새 메뉴는 [+ 메뉴]로 추가한다.
3. 대시보드 오른쪽 「월 판매 계획」에서 메뉴별 예상 월 판매량을 고친다.
4. 왼쪽 대시보드에서 이번 달 이익(적자), 손익분기 판매량·매출액, 고정비 회수율, 손해 메뉴 수를 확인한다. 1잔 이익이 0원 이하인 메뉴는 카드에 경고가 뜬다.
5. 카드는 고른 정렬 기준(기본: 매출 비중) 순서다. 값을 고쳐도 카드는 제자리에 있고, [다시 정렬]을 누르면 바뀐 값으로 다시 줄을 세운다.
6. 「시나리오 비교」 탭에서 "가격을 바꾸면 한 달에 얼마나 남을까?"를 따져 본다. A안·B안마다 판매가를 몇 % 바꿀지, 그러면 판매량이 몇 % 바뀔지 정하면 각 안의 월 이익과 "지금보다" 차이, 손익분기·회수율 표가 보인다. 각 안 아래의 판매량 기준(예: "판매량이 최대 12.1% 줄어도 지금만큼 남습니다")보다 예상이 좋으면 지금보다 남는다.

입력한 값은 저장되지 않는다. 새로고침하면 예시 메뉴로 돌아간다.

용어: 1잔 이익 = 판매가÷1.1 − 원가 − 수수료. 원가율 = (원가+수수료)÷판매가. 마진율 = 1잔 이익÷판매가. 고정비 회수율 = 메뉴를 팔아 남긴 돈÷월 고정비(100% 이상이면 흑자).

## Work process

## Claude Code evidence

## Three effective practices

## Three difficulties
