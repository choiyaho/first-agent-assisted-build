# PLAN

> Claude Code가 SPEC.md를 읽고 제안 → 학생이 고치고 승인한다. 승인 전에는 구현하지 않는다.
> 상태: 대기 / 진행 / 확인 대기 / 완료 / 보류
> 「완료」로 바꾸는 것은 학생이다.

## 단계

| # | 단계 | 완료 기준 (SPEC 4번 #) | 확인 방법 | 상태 | 커밋 |
|---|---|---|---|---|---|
| 1 | `calc.py`(계산 함수) + `check_calc.py`(C1~C4, E1, E2) | #5 | `python src/check_calc.py` → `check ok` | 확인 대기 | |
| 2 | `.venv` 재생성, `requirements.txt`, streamlit 설치, `app.py` 화면 (사이드바·숫자 카드·메뉴 탭·시나리오 탭) | #1~4 | `streamlit run src/app.py`에 C1·C2·C3·E1 입력 → SPEC 값과 같음 | 대기 | |
| 3 | 화면 스크린샷, README (학생) | — | — | 대기 | |

## 진행 기록

단계마다 Claude가 보고를 추가하고, 학생이 확인과 결정을 쓴다. README·회고·영상의 원재료다.

### 단계 N: YYYY-MM-DD

- Claude 보고:

      (CLAUDE.md「단계 보고」형식)

- 내가 확인한 것:
- 결정: 유지 (커밋 ) / 폐기 (restore) / 다시 지시 (무엇을)
- 증거 후보: (스크린샷 파일명, 무엇을 보여주는지)

### 단계 1: 2026-10-20

- Claude 보고:

      [단계 1 보고]
      바꾼 파일: calc.py(새), check_calc.py(새), PLAN.md(단계표·진행 기록)
      한 일: 1잔 이익·원가율·마진율, 가게 전체 손익분기(잔 수·매출액), 시나리오 % 적용, 원 단위 사사오입 함수를 calc.py에 작성.
             check_calc.py가 SPEC 5번 C1~C4, E1, E2 기대값과 비교.
      세운 가정: 계산은 Fraction으로 정확히, 반올림은 표시용 round_won/pct1에서만. 수수료율은 % 숫자(2 = 2%).
                 판매가 0이면 비율은 None(화면에서 "-"). 손익분기 없음은 be_cups=None + reason 문자열.
      확인 방법: python3 src/check_calc.py → check ok
      내가 실행한 명령과 실제 출력:
        $ python3 src/check_calc.py → check ok
        $ python3 -c "from calc import round_won; print(round_won(2.5), round_won(-2.5), round_won(2.4))" → 3 -3 2
      제안 커밋 메시지: feat: 계산 함수(calc.py)와 손 계산 사례 검사(check_calc.py) 추가

- 내가 확인한 것:
- 결정: 유지 (커밋 ) / 폐기 (restore) / 다시 지시 (무엇을)
- 증거 후보:

## 바뀐 결정

SPEC이나 계획을 바꾸면 여기에 남긴다.

| 날짜 | 무엇을 | 왜 |
|---|---|---|
| 2026-10-20 | SPEC.md를 Claude가 초안 작성 (CLAUDE.md 규칙 1 예외) | 학생 지시. 일정 지연(마감 D-12)으로 빠르게 진행 |
| 2026-10-20 | D1 (b) 재료 환산 → (a) 1잔 원가 직접 입력, D6 본인 인건비 칸 제거, D7 시나리오를 % 슬라이더로 | 범위 축소. 교수님 코멘트 "기능은 간단, UI/UX에 힘을" |
| 2026-10-20 | 손 계산 사례를 Claude가 검산 쉬운 숫자로 작성, 학생은 검산만 | 학생이 손 계산 생략을 원함. 검증 근거는 남기기 위해 최소한으로 유지 |
| 2026-10-20 | 폴더 정리: 소스 `src/`, 문서 `docs/`. CLAUDE.md·README.md는 루트 | 학생 지시. 실행 경로는 `python src/check_calc.py`, `streamlit run src/app.py` |
