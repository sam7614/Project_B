# 합성 학생 데이터 생성·활용 프로토콜

## 결정 및 적용 범위

2026-10-25, 연구자의 지시에 따라 실제 학생 자료가 없는 개발 단계에서 완전 합성 데이터를 사용한다. 실제 학생 원자료를 학습하거나 재표집하지 않는다. 이 프로토콜은 소프트웨어·설계 검증을 위한 방법 보완이며, 선정 계획서의 실제 요구조사·FGI·전문가/사용자 평가를 수행한 것으로 대체하지 않는다. 연구 범위 변경이 필요하면 연구자가 기관 절차를 확인한다.

## 선행연구 검토와 사례 수

- Agal, S. (2026). *A privacy preserving synthetic learner dataset for learning analytics in technology enhanced higher education*. Scientific Reports, 16, 14772. https://doi.org/10.1038/s41598-026-44990-8
  - 발행일 2026-03-23. 원문 Abstract·Major contributions에서 합성 학생 20,000건, 85개 변수를 확인했다.
  - 초기 20,000건 생성의 규모 참고로 사용했다. 이후 사용자의 학교 규모 요청에 따라 현재 코호트는 총1,000명으로 축소했다. 선행연구의 실제 자료 기반 생성 방법·차등 개인정보보호·충실도·예측 결과를 재현하거나 차용했다고 주장하지 않는다.
- Tiukhova et al. (2026). *Real Enough to Matter? Implications of Synthetic Data for Reproducible Learning Analytics*. EDM 2026 proceedings. https://educationaldatamining.org/edm2026/proceedings/2026.EDM.full-papers.114/index.html
  - 원문 Abstract 및 RQ1–RQ3에서 실제 자료와의 유사성, 예측 유용성, 기존 해석 결과의 재현을 구분한 평가 접근을 확인했다.
  - 본 연구는 실제 비교 자료가 없으므로 그러한 충실도·전이·재현을 검증했다고 쓰지 않는다.

두 원문 확인일: 2026-10-25. 제한적 탐색으로 찾은 사례이며 체계적 문헌고찰이나 분야 전체의 최대 규모 조사 결과가 아니다. 표본 수를 늘려도 실제 학생에 대한 대표성이나 검정력이 확보되지 않는다.

## 데이터 구성

- 현재 전체 합성 코호트·앱 표시: **총1,000명**, 실제 참여자0명. 2026-10-25 사용자의 규모 축소 요청을 반영했다. 전체 학년 합계에 대한 설정이며 실제 재적 수 추정이 아니다. 생성기의 기본값·상한은1,000건이다.
- 독립 교차 fixture:256건. 4학년 × 4개 대표 모듈 × 16개 상황의 조합을 점검하는 하위 집합이며, 현재 앱 전체 표시 인원은1,000명이다.
- 시트의 기존 첫1,000개 ID와 값은 보존하고 나머지 행을 제거했다. 보존된1,000명 전원을 active로 설정했다. 시트 편집값을 생성기 원본으로 다시 덮어쓰지 않는다.
- 별도 음성/공격 사례: 잘못된 이수율, GPA, 학점, 모듈 결측, 중복 ID, 상담 입력의 명령문 등 6건. 정상 코호트와 분리한다. 사례 생성 자체는 앱의 거부·보안 동작 검증 완료를 의미하지 않는다.
- 시드: 20261025. LCG의 상태·상수는 생성 코드에 명시했다. 날짜 기준은 2026-10-25이며 실행 시각을 데이터에 주입하지 않는다.
- 학년·모듈·상황은 설계한 교차 배치다. 나머지 점수와 학점 일부는 고정 시드의 범위 내 임의 값이다. 실제 모집단 분포·상관·결측 기제를 추정한 데이터가 아니다.
- 이수율 = 모듈 취득학점 / 모듈 요구학점 18 × 100의 반올림. 총 취득학점은 졸업 요구학점 130 이내다. **18/130학점은 데모 가정이며 실제 대학 규정이 아니다.**
- 점수·출석·관계·정서·진로는 서로 타당화된 척도가 아니다. 상태는 시나리오 분기 표시이며 임상·심리 또는 학업 위험의 진단이 아니다.

## 16개 상황

| 코드 | 검토 목적 |
| --- | --- |
| normal | 일반 이수 현황 |
| low-progress | 낮은 이수율 표시 |
| requested | 상담 요청 상태 |
| waiting | 상담 대기 상태 |
| completed | 모듈 이수율 100% 경계 |
| near-completion | 모듈 완료 직전 |
| career-undecided | 진로 목표 공란 |
| reflection-missing | 성찰 기록 결측 |
| plan-changed | 설계 변경 사유 |
| prerequisite-gap | 선수요건 불충족 |
| credit-overload | 가정한 학기 계획학점 초과 |
| inactive | 출석 입력 0과 상담 기록 없음 |
| high-achievement | 높은 성취 가정의 과업 식별자; 점수 우수성 판정이 아님 |
| cross-module | 복수 모듈 선택 |
| new-entry | 모듈 학점·이수율 0 경계 |
| data-review | 교수자 자료 확인 필요 |

현재 `high-achievement`는 명명된 과업 식별자에 불과하고 모든 점수는 동일 40~100 범위에서 생성한다. 실제 고성과 집단 또는 진단 결과로 분석하지 않는다. 각 확장 필드의 앱 동선 구현 여부는 별도 추적한다.

## 필드 사전

| 필드 | 형식·의미 |
| --- | --- |
| id, studentId, name | SYN-숫자7자리, 동일 가상학번, 가상학생 명칭 |
| synthetic, datasetVersion, scenario | true, pb-synthetic-v1, 상황 코드 |
| department, grade, module | 데모 학과, 1~4, 대표 모듈 문자열 |
| selectedModules | 선택 모듈 배열; 대표 모듈별 통계는 module만 집계 |
| moduleCreditsEarned, moduleCreditsRequired, progress | 모듈 취득학점, 요구학점18, 계산 이수율0~100 |
| creditsEarned, totalCredits, generalProgress | 총 취득학점0~130, 요구학점130, 계산 백분율 |
| gpa | 1.00~4.50의 임의 값; 실재 성적 아님 |
| attendance | 0 또는60~100, 임의 출석 입력 |
| midtermScore, finalScore, assignmentScore, projectScore | 각각40~100의 독립 임의 점수 |
| participationScore, socialScore | 각각40~100의 임의 UI 입력; 참여·사회성 측정 척도 아님 |
| status | Good / Warning / Request / Waiting; 생성 상황에 따른 데모 분기 |
| careerGoal, missingFields | 임의 진로 또는 공란, 명시적으로 비운 필드 이름 배열 |
| prerequisiteMet, plannedSemesterCredits | 선수요건 가정, 계획학점18 또는24 |
| planChangeReason, reflection, reviewRequired | 합성 설계변경·성찰 문자열 또는null, 확인필요 플래그 |
| lastConsultation, consultations | null 또는 기준일 이전의 합성 일자; 합성 상담 배열 |
| consultations 내부 | id/date/synthetic/note/nextAction/professorDecision. 모두 예시이며 실제 상담·교수자 평정이 아님 |
| analysis, aiSummary, consultationTopics | 명시적으로 합성 표시한 템플릿. LLM 출력 또는 인간 평정 아님 |
| email, phone | example.invalid 주소, 비전화 문자열; 실제 연락처 없음 |
| peerGroup, avatarColor | 기본 빈 관계 배열, 표시 색. 앱 변환 시 고정 같은 학년 고리 관계 추가 |

CSV는 위 JSON 중 명시된 17개 요약 필드만 내보낸다. 완전한 필드는 JSON에 있다.

## 생성·검증·보관

연구 저장소 루트에서 Node.js로 실행한다. 외부 패키지·API·개인정보 입력이 필요 없다.

    node scripts/generate-synthetic-students.cjs
    node scripts/verify-synthetic-students.cjs

생성 위치는 `.synthetic-data/`이며 전체 JSON/요약 CSV/데모 JSON/별도 음성 사례/manifest가 있다. 대용량 생성물은 Git에서 제외하고 생성 코드·검증 코드·이 프로토콜을 추적한다. manifest는 시드, 규칙, 생성기 SHA-256, 산출물별 SHA-256·바이트, 상황별 수를 기록한다. 옵션 `--count`, `--seed`, `--out`으로 별도 버전을 만들 수 있다.

현재 확인 결과:1,000건의 고유 ID·범위·학점-이수율 일치·결측 표기·합성 표시·파일 해시,256건의 교차 조합 검사를 통과했다. 같은 시드로 재생성한1,000건 학생 JSON의 바이트 단위 해시가 일치했다. 실제 데이터 충실도·외적 타당성·공정성·추천 성능을 검증한 결과가 아니다.

## 보고서·논문에 사용할 표현

“실제 학생 원자료를 사용하지 않고 모듈 이수와 상담 과업의 기술적 점검을 위해 합성 자료를 구성하였다. 초기20,000건으로 생성했으나 학교 규모에 맞추라는 연구자의 요청에 따라 현재 총1,000명으로 축소하고, 수정 가능한 구글시트와 앱에 연결하였다.256건의 학년·모듈·상황 교차 fixture는 별도의 하위 점검 집합이다. 합성 사례는 실제 참여자 수나 요구조사 응답 수에 포함하지 않았다. 관찰 결과의 범위는 구현·동기화·시나리오 검증이며 교육 효과나 모집단 요구의 추론으로 확장하지 않았다.”

가상 설문으로 t/Borich/LF 계산 코드를 실행한다면 분석 파이프라인 점검이라고 명시하고 실제 요구도 결과 장의 통계로 수록하지 않는다. 같은 규칙으로 생성한 라벨과 판정의 일치는 순환 검증이므로 추천의 교육적 타당성 근거로 사용하지 않는다.
