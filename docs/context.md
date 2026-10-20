# context.md — calffeine 세션 요약 (2026-10-20)

> 다음 세션에서 이어서 작업할 때 읽는 인수인계 메모. 규칙 원문은 CLAUDE.md, 결정은 SPEC.md, 진행은 PLAN.md가 기준이다. 이 파일과 다르면 그쪽을 따른다.

## 1. 지금 상태 한 줄
문서(SPEC·CLAUDE·PLAN)는 "레시피 원가 + 네이버 쇼핑 API·NVIDIA LLM 단가 검색" 계획으로 수정 완료. 코드는 아직 옛 화면(손익분기·시나리오) 그대로. **PLAN 단계 3~5 학생 승인 대기.**

## 2. 과제와 역할
- DIGB339「Project 1: First agent-assisted build」개인 과제, 마감 2026-11-01 23:59 KST
- 저장소와 결정의 주인은 학생. Claude는 승인된 한 단계씩만 구현하고 「단계 보고」 후 멈춘다
- 앱 calffeine: 소규모 카페 사장용 Streamlit 앱

## 3. 이번 세션에서 바뀐 방향
- 메뉴 하나를 고르고 희망 판매가를 넣으면 `recipe.csv` 레시피 × 재료 단가 + 포장비(공통 300원)로 1잔 원가를 계산하고, 1잔 이익·원가율·마진율을 보여준다
- 재료 단가는 **네이버 쇼핑 검색 API + NVIDIA 무료 LLM**으로 찾는다 (처음엔 Claude API sonnet → 학생이 무료 API로 변경)
- 손익분기·시나리오 탭은 **보류** (calc.py 함수와 check_calc 사례는 남김)
- 학생 확인 사항: 공지는 외부 API를 금지하지 않음(키 커밋만 금지). Claude Pro 구독에는 API 크레딧이 없음

## 4. 꼭 지킬 규칙 (요점, 원문은 CLAUDE.md)
- SPEC 빈칸·정의 결정에 걸리면 질문. SPEC.md는 고치지 않음 (이번 수정은 학생 지시로 예외, PLAN「바뀐 결정」에 기록)
- 승인 전 코드 변경 금지, 한 번에 한 단계, git add/commit/push/restore 실행 금지(커밋 메시지는 제안만)
- PLAN에 없는 새 파일·패키지·삭제·저장소 밖 접근은 먼저 묻기
- API 키(`NAVER_CLIENT_ID`, `NAVER_CLIENT_SECRET`, `NVIDIA_API_KEY`)는 셸 환경변수로만. .env·secrets 파일 만들거나 읽지 않음. 키를 코드·문서·출력에 쓰지 않음
- 외부 API 실제 호출은 Claude가 실행하기 전에 묻기
- 단가 검색 결과(실제 판매처·가격)는 화면에만, 저장·커밋 금지
- check_calc.py 기대값은 SPEC 5번에서만. LLM 결과는 기대값으로 쓰지 않음
- 경계 사례(판매가 ≤ 변동원가, 판매량 0, 빈 입력, 음수, 단가 빈 칸·구매량 0, API 키 없음, 검색 실패)는 멈추지 않고 이유 표시
- README의 「Work process」「Claude Code evidence」「Three effective practices」「Three difficulties」는 학생이 씀. Claude는 요청 시 「How to run / use」 초안만

## 5. 기술 구성
- Python 3.12.7(python.org 설치) + `.venv/`, Streamlit 1.66.0, pandas(streamlit 의존성). requirements.txt는 `streamlit` 한 줄
  - brew python@3.12(3.12.15)도 설치돼 있음. 삭제는 제안만 했고 실행 안 함
- 계산은 `fractions.Fraction`, 반올림은 표시할 때만 (`round_won` 사사오입, `pct1` 소수 1자리)
- 계획된 `price_agent.py`: 재료마다 네이버 쇼핑 검색 → NVIDIA LLM이 관련 상품을 거르고 상품명에서 구매량(g/ml)을 읽음 → 단위당 최저가 상품의 구매가·구매량·링크 반환. `urllib`로 호출, 패키지 추가 없음
- 실행: 키 3개 `export` → `streamlit run src/app.py`. 키가 없어도 앱은 돌고 단가 직접 입력 가능

## 6. 파일 현황
| 파일 | 상태 |
|---|---|
| `src/calc.py` | 단계 1. fee, profit_per_cup, cost_ratio, margin_ratio, summary(손익분기), apply_scenario, round_won, pct1 |
| `src/check_calc.py` | 단계 1. C1~C4, E1, E2 검사 → `check ok`. "라떼" 이름은 SPEC 사례라 유지 |
| `src/app.py` | 단계 2의 옛 화면(사이드바·숫자 카드·메뉴별 마진·시나리오 탭). `menu.csv`를 읽음. 단계 5에서 메뉴 조회 화면으로 교체 예정 |
| `src/menu.csv` | 가상 예시 메뉴 12개 (메뉴, 판매가, 1잔 원가, 월 판매량) |
| `src/recipe.csv` | 12개 메뉴 레시피 46행 (메뉴, 재료, 용량, 단위). 아이스 1잔(약 400ml) 기준, 포장재 제외. 두 CSV 메뉴 이름 일치 확인함 |
| `docs/SPEC.md` | 새 계획으로 수정. D1 (c), D2 포장비 300원, D5~D7 보류, D10·D11 추가, 손 계산 사례 R1·R2·E3·E4·E5 (학생 검산 ☐) |
| `docs/PLAN.md` | 단계 1·2 확인 대기, 단계 3~5 승인 대기 |
| `CLAUDE.md` | 규칙 7·8, 검증 규칙, 기술 구성 수정 |
| `README.md` | 3행 목적 설명과 15~23행 How to run이 옛 흐름. 학생 문서라 Claude는 안 고침 |

## 7. PLAN 단계표 (요약)
| # | 단계 | 완료 기준 | 상태 |
|---|---|---|---|
| 1 | calc.py + check_calc.py(C1~C4, E1, E2) | #6 | 확인 대기 |
| 2 | .venv, requirements, app.py(옛 화면) | SPEC 개정 전 #1~4 | 확인 대기 |
| 3 | calc.py에 레시피 1잔 원가 함수, check_calc.py에 R1·R2·E3·E4 추가 | #1·2·4·6 | 승인 필요 |
| 4 | price_agent.py: 네이버 쇼핑 → NVIDIA LLM → 단위당 최저가 | #3·5(E5) | 승인 필요 |
| 5 | app.py를 메뉴 조회 화면으로 교체, 손익분기·시나리오 탭 제거 | #1~5 | 승인 필요 |
| 6 | 스크린샷, README (학생) | — | 대기 |

## 8. 손 계산 사례 (SPEC 5번, 공통: 수수료 2%, 포장비 300원)
- R1 아메리카노: 원두 25,000원/1,000g, 물 0원/1,000ml, 얼음 5,000원/3,000g → 재료비 700, 원가 1,000. 희망가 4,400 → 1잔 이익 2,912원, 원가율 24.7%, 마진율 66.2%
- R2 카페라떼: 우유 2,900원/900ml → 원가 1,644원. 희망가 5,500 → 3,246원, 31.9%, 59.0%
- E3: R1에 희망가 1,000 → −111원, 원가율 102.0%, 마진율 −11.1%, 손해 경고
- E4: 얼음 구매량 0 → "계산 불가 — 단가가 없는 재료: 얼음"
- E5: 키 없음 → "검색 키가 없어 검색할 수 없음 — 단가를 직접 입력하세요"

## 9. 남은 일
학생:
1. SPEC 5번 R1·R2·E3 검산
2. PLAN 단계 3~5 승인 (또는 수정 지시), 단계 1·2 「내가 확인한 것」「결정」 기록
3. 키 발급: 네이버 개발자센터 검색 API(Client ID/Secret), build.nvidia.com API 키. 단계 4 전까지

단계 4에서 정할 것:
- 레시피의 "물"을 검색하면 생수가 나옴 → 검색에서 뺄지, 0원으로 둘지
- NVIDIA 모델 이름 (SPEC D10에 기록)
- NVIDIA 무료 한도·조건, 네이버 쇼핑 API 엔드포인트·하루 호출 한도 확인

그 외:
- 단계 5 이후 요청 시 README 「How to run / use」 초안
- `brew uninstall python@3.12`는 학생 지시가 있을 때만

## 10. 참고
- git: 최근 커밋 `c5a191b Docs : 계획 문서 수정 및 메뉴/레시피 문서 업데이트`, 이 파일 만들기 전 작업 트리 깨끗함
- 해결한 문제: AppTest 상대경로 오류 → 절대경로 / `use_container_width` 폐기 경고 → `width="stretch"` / brew가 3.12.15를 받아 python.org 3.12.7로 .venv 생성
- AppTest 기본 화면 결과(동작 확인용, SPEC 기대값 아님): 3,347,704원 / 1,552잔 / 8,015,977원, 예외 없음
