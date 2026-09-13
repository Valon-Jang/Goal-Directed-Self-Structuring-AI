# E001 연구 재개점 — 2026-09-13

Repository: Valon-Jang/Goal-Directed-Self-Structuring-AI.
Branch: research/e001-goal-vs-human-v01.

먼저 experiments/E001/RUNBOOK.md와 PROTOCOL.md, evidence/E001/E0_RESULT.json을 읽는다. 원래 이론은 README.md와 docs/RESEARCH_SCOPE.md에 보존했다.

## 완료

- 연구 목표와 BARE-GOAL(사용자 표기 ARE-GOAL) / HUMAN-GUIDED 비교 정의.
- 성과·전체 사람시간·비용·질문·재작업·실제 Capability 재사용 측정 프로토콜.
- 합성 개발업무 3종×4개 변형, 독립 정답 계산, 읽기 전용 도구 환경.
- 36개 E0 자동검사 실제 PASS; 기준 fixture 48회, 전이 검사 12건.
- GitHub Actions run 34755692760 / job 103719558829의 완료 상태와 로그 확인.
- 테스트한 코드 커밋: 54fcd6977c73b34c2e400c57cdce45386f2ab46b. 이후 문서·근거 추가는 이 해시를 소급 변경하지 않는다.

## 금지할 오해

실제 AI 2조건 비교는 0회다. 실제 인간 방법서 0건이다. 비용·인간 개입시간을 측정한 것처럼 만들지 않는다. E0 fixture의 성공을 BARE-GOAL이나 HUMAN-GUIDED의 성공률로 부르지 않는다. AI가 인간인 척 작성한 방법서를 HUMAN_AUTHORED로 표시하지 않는다.

## 다음 실행 단위

E0.1: 실제 동일 모델을 독립 세션으로 호출하는 bounded adapter와 전체 인간시간 수집기를 검증한다. 요청 전 budget enforcement와 backend identity를 근거로 확인한다. 탐색용 동기 callback만으로는 본실험에 진입하지 않는다.

동시에 진짜 인간 작성 방법서/준비시간/개발자료만 열람했다는 출처를 확보한다. 이 필수 인간 입력은 AI가 대신 날조할 수 없다. 그 다음 계획·설정·평가기 동결 → 새 held-out 12 A/B 업무쌍 → 216개 파일럿 trajectory → 실패 포함 분석 순서다.

완료 판정의 목적은 AI 자율 방식의 승리를 연출하는 것이 아니라, 인간의 방법 설계가 유효한 조건과 불필요한 조건을 구분하는 것이다.
