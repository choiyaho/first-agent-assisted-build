# CLAUDE.md

이 저장소는 DIGB339「Project 1: First agent-assisted build」개인 과제다.
저장소와 결정의 주인은 학생이다. 너(Claude Code)는 학생의 지시에 따라 한 단계씩 구현을 돕는다.

## 세션 시작 시
1. docs/SPEC.md와 docs/PLAN.md를 읽는다.
2. 지금 진행 중인 단계와 다음 할 일을 한 줄로 말하고 지시를 기다린다.

## 역할
- 학생: 범위와 정의 결정(SPEC.md), 계획 승인, diff 검사, 커밋·push·restore, 검증 확인, README 작성
- Claude: 질문, 가정 제시, 계획 제안, 승인된 한 단계 구현, 실행 결과 보고

## 작업 규칙
1. SPEC.md의 빈칸이나 「2. 정의 결정」에 달린 일이면 구현하지 말고 그 항목을 질문한다. 추측해서 정하지 않는다. SPEC.md는 고치지 않는다.
2. PLAN.md 단계표가 승인되기 전에는 코드 파일을 만들거나 바꾸지 않는다. 계획을 제안할 때 세운 가정을 함께 나열한다.
3. 한 번에 PLAN.md의 한 단계만 한다. 끝나면 「단계 보고」를 하고 멈춘다. 학생이 다음 단계를 지시하기 전에는 진행하지 않는다.
4. PLAN.md 단계에 적히지 않은 새 파일 생성, 패키지 추가·설치, 파일 삭제, 저장소 밖 접근은 먼저 묻는다.
5. git add / commit / push / restore를 실행하지 않는다. 커밋 메시지는 제안만 한다.
6. 다른 프로젝트·튜토리얼·템플릿의 코드를 가져오지 않는다.
7. 이 프로젝트는 API 키가 필요 없다. .env를 만들거나 읽지 않는다.
8. 예시 데이터는 가상의 값만 쓴다. 실제 가게·사람 정보를 넣지 않는다.

## 단계 보고
단계가 끝나면 아래 형식으로 답한다. 같은 내용을 PLAN.md「진행 기록」에 추가하고, 그 단계 상태를「확인 대기」로 바꾼다.
「내가 확인한 것」「결정」줄은 비워 두고, 상태를「완료」로 바꾸지 않는다. 학생이 쓴다.

    [단계 N 보고]
    바꾼 파일:
    한 일 (3줄 이내):
    세운 가정:
    확인 방법 (학생이 실행할 명령 → 기대 결과):
    내가 실행한 명령과 실제 출력:
    제안 커밋 메시지:

## 검증 규칙
- "완료됐다"는 말 대신 실행한 명령과 실제 출력을 보여준다.
- check_calc.py의 기대값은 SPEC.md「5. 손 계산 사례」에서만 가져온다. calc.py를 실행해 나온 값을 기대값으로 쓰지 않는다.
- 검사가 실패하면 고치기 전에 실패 내용을 먼저 보고한다.
- 경계 사례(판매가 ≤ 변동원가, 판매량 0, 빈 입력, 음수)는 오류로 멈추지 않고 화면에 이유를 보여준다.
- 올림·나눗셈은 정수로 곱한 뒤 마지막에 한 번 나눈다. 소수 가중평균 뒤 올림하지 않는다.

## 기술 구성
(권장안. 학생이 바꾸면 이 섹션을 고친다.)
- Python 3.12 + Streamlit 1.66.0, 가상환경 `.venv/`
- 폴더: 소스는 `src/`, 문서(SPEC·PLAN·구상)는 `docs/`. CLAUDE.md·README.md·requirements.txt·`.streamlit/config.toml`(화면 테마)는 루트
- `calc.py`: 계산 함수만. Streamlit을 import하지 않는다.
- `app.py`: 화면. 계산은 calc.py 함수를 호출한다. 화면 코드 안에서 직접 계산하지 않는다.
- `check_calc.py`: `python src/check_calc.py` → 모든 사례 통과 시 `check ok`, 실패 시 어떤 사례가 기대값과 다른지 출력
- `requirements.txt`: `streamlit==1.66.0` (배포 서버가 로컬에서 검증한 버전을 설치하도록 고정). 그 외 패키지는 묻는다.
- 실행: `streamlit run src/app.py`
- 배포: Streamlit Community Cloud (main 브랜치, `src/app.py`, Python 3.12, SPEC D14). main에 push하면 자동으로 다시 배포되므로 push 전에 `check ok`와 화면 확인을 한다. 배포 설정은 학생이 웹에서 한다.
- 금액은 원 단위. 비율 자릿수와 반올림은 SPEC.md 정의 결정 D8을 따른다.
- 코드는 학생이 디펜스에서 설명할 수 있게 짧고 단순하게 쓴다. 함수마다 한 줄 설명을 단다.

## 문서
- README.md의「Work process」「Claude Code evidence」「Three effective practices」「Three difficulties」는 쓰지 않는다. 학생이 쓴다.
- 요청받으면「How to run / use」초안만 쓸 수 있다.
- 커밋하면 안 되는 것: .env, .venv/, __pycache__/, 영상(*.mp4, *.mov), 대용량 데이터, 개인정보.
