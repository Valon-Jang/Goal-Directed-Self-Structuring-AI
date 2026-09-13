# E001 연구 재개점 — E0.1 실제 모델 실행 후

Repository: Valon-Jang/Goal-Directed-Self-Structuring-AI.
Branch: research/e001-goal-vs-human-v01. PR #1.

먼저 RESEARCH_CHARTER.md → experiments/E001/E01_FINDINGS.md → evidence/E001/E01_RESULT.json을 읽는다. 본래 비교 설계는 experiments/E001/PROTOCOL.md, 원래 이론은 README.md와 docs/RESEARCH_SCOPE.md에 보존했다. RUNBOOK.md의 E0 기록은 해당 시점의 이력이며, 최신 측정은 E01_RESULT.json을 우선한다.

## 사용자 확정 방향

사용자는 이 저장소를 AI의 지속적인 실험 공간으로 지정했고, 목표가 현재 구조에 머무르지 않고 계속 발전하도록 연구를 위임했다. 다음 단계 선정·설계·가역적 저위험 실험·코드·근거 기록을 능동적으로 진행한다. 새 유료 자원, 고객 원본·외부 발송, 공개 범위 확대, 권한 확대는 이 위임에 포함하지 않는다. 예약 또는 상시 백그라운드 실행이 설정된 것은 아니다.

## 완료와 근거

- E0: 36개 검사 PASS; 기준 계산 fixture 48회, SQL 전이 검사 12건. 테스트 커밋 54fcd6977c73b34c2e400c57cdce45386f2ab46b, run 34755692760.
- E0.1 측정 구현: 적극적 사람시간 집계, 누락 null 보존, 중단 호출 재실행 방지 ledger, 216개 균형 실행 순서 생성기, 업무 단위 묶음 통계, 모호한 JSON 도구 실행 거부.
- E0.1 원격 검사: 기존 36 + 새 22 = 58개 PASS. run 34756883943/job 103722672201.
- E0.1 실제 모델: Qwen3-0.6B Q8_0 + llama.cpp b10344, CPU, 업무별 별도 프로세스. 실제 호출 15회/응답 15회, 3개 공개 개발 업무 모두 실패(0/3). 입력 14,465 + 출력 520 = 14,985 tokens. 오류 반복·동일 조회 반복·빈 제출을 관찰했다.
- 실제 모델 테스트 커밋은 9d2eac8c9b9458418cef1eb98224629b6fb98cee다. 이후 분석·재생 센서 추가가 이 실험 조건을 소급 변경하지 않는다.
- 실패 trace 기반 반복 센서를 추가하고 로컬 검사를 수행했다. 이것은 관찰용·사후 재생이며 실행 중 절감 효과를 검증한 것이 아니다. 원격 전체 검사 결과는 해당 PR의 정확한 후속 commit/check 상태로 확인한다.

## 여전히 0 또는 미측정

실제 BARE-GOAL vs HUMAN-GUIDED 본실험 0회, 실제 인간 작성 방법서 0건. 인간 총개입시간과 CPU 전체 비용은 미측정이다. 단순한 모델 호출이나 CI 성공을 업무 성공으로 표현하지 않는다. 본실험 216회는 아직 계획이다. AI가 인간인 척 작성한 방법서는 사용하지 않는다.

## 다음 실행 단위

E0.2는 E01_FINDINGS.md의 prospective plan부터 시작한다. 먼저 실제 렌더링 prompt/도구 schema 전달, 거부된 action의 안전한 진단, unknown-argument 차단, 강제중단·프로세스 정리의 fault probe를 검증한다. 그 뒤 version 번호까지 의미 있게 변형된 새 개발 사례에서 모델·목표·권한·예산을 고정하고 도구 인자 schema의 명확성만 바꿔 24개 진단 trajectory를 비교한다. 원래 E001 인간 비교와 혼합하지 않는다.

반복 센서는 우선 OBSERVE_ONLY다. 모델 크기·schema·중단 정책을 동시에 바꾸지 않는다. 현재 작은 모델의 바닥 수준 결과로 대형 모델이나 Goal Engineering의 한계를 결론 내리지 않는다. 인간 방법서가 아직 없더라도 실행·측정·Capability 전이 연구는 별도로 진행한다.

## 운영 경험

GitHub Models는 현재 종료된 서비스이므로 과거 ai-inference/GITHUB_TOKEN 예제로 호출을 재시도하지 않는다. 공식 모델 commit + GGUF SHA, llama.cpp release archive SHA를 고정해 GitHub 표준 CPU runner에서 가져와 실행한 경로는 이번 범위에서 검증됐다. connector의 workflow 파일명 runs URL은 허용되지 않았고, actions/runs?event=push&branch=... 조회 후 전용 job/log 도구를 쓰는 경로가 동작했다. 로컬 Chat 실행환경의 git clone은 DNS 연결 실패였으며 같은 경로를 무작정 반복하지 않는다.

정상 실행은 종료됐고 상주 모델 서버나 정기 모델 실행을 남기지 않았다. 공개 저장에는 일반 연구와 합성 자료만 사용한다. raw call ledger의 byte-identical 보관은 완료하지 않았으며 정규화된 도구 trace와 실행기 보고 해시를 별도로 보존했다.
