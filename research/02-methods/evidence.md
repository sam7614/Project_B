# Ⅱ. 연구 방법과 수행 · 근거 자료 목록

## E-NA-003. 사전 자료·KCI벤치마킹과 전체 설문 원문

2026-10-27 사용자 요청 반영. 선정계획서PDF10·11·14쪽과 기존FGI질문지를 다시 읽고, 사전 자료8종의 확보 상태/활용을 정리했다. KCI5편의 등재·서지·공개 초록 및 해외2편의 공개 본문을 확인했다. 원문 확보 실패 범위는needs-analysis-prerequisites.md와research/data/needs-benchmark-sources.json에 명시했다. 교수자/관리자·학생용 각각배경6문항·핵심12쌍·우선1·개방형3문항을 자체 작성했다. 코드북/자료·문항·과업 대응은needs-instrument-design.md, 전체 원문은survey-faculty-v1.md / survey-student-v1.md 및JSON기준본에 있다. 실제 조사·타당화·승인이나 표본수 확보를 수행한 것은 아니다. 보고서v0.8의3·5·16·17절에 반영했다.

## 등록 원칙

- ID, 연결 본문, 서지 또는 산출물명, 원문 URL/DOI, 인용 위치, 확인일, 확인 상태를 기록합니다.
- 계획서에 열거된 참고문헌도 원문과 서지를 확인한 후 등록합니다.
- 참여자 식별자료와 비공개 원자료는 저장소에 올리지 않고 승인된 보관 위치만 기록합니다.

## 근거 기록 양식

### 근거 ID: 작성 예정

- 연결 본문:
- 저자·기관 / 연도 / 제목:
- URL 또는 DOI:
- 근거 위치 (쪽·문단·표):
- 확인일 / 확인 상태:
- 핵심 내용:
- 연구에 반영한 내용:

## E-SYN-001. 완전 합성 학생 데이터 생성 프로토콜

- 확인일: 2026-10-25
- 문헌: Agal (2026), Scientific Reports 16, 14772, https://doi.org/10.1038/s41598-026-44990-8 (Abstract·Major contributions의20,000건·85변수 규모 확인).
- 평가 방법 참고: Tiukhova et al., EDM2026, https://educationaldatamining.org/edm2026/proceedings/2026.EDM.full-papers.114/index.html (Abstract·RQ1–RQ3).
- 반영 범위: 생성 규모의 참고와 검증 영역 구분. 해당 논문의 방법·효과·개인정보보호 보장을 본 데이터에 귀속시키지 않는다.
- 자체 산출물: [합성 데이터 프로토콜](synthetic-data.md), scripts/generate-synthetic-students.cjs, scripts/verify-synthetic-students.cjs.
- 상태: 공개 원문 확인 및 자체 생성·제약·재현 검사 수행. 실제 데이터 충실도·실증 연구 결과 미검증.

## E-NA-001. 요구분석 개발 fixture와 계산 검증

2026-10-25 19시 수행. 가상ID4×항목3의12행, 실제 응답자0명. 입력 계약·Borich/LF·t통계량 산술 및 오류/경계의 단위 검사7개 통과. p값·CI·가정 검토·실증 분석은 미실행. [실행·출처·한계](needs-analysis-readiness.md). v0.4→v0.5 보고서6절에 반영하고 원고 스냅샷 및 일일 구글독스에 기록했다.

## E-NA-002. 요구조사 코드북 초안과 LF 개발 그림

2026-10-27 오전 실제 수행. [코드북 초안](needs-codebook-draft.md)의12문항은 미확정·미타당화 상태이며 실제 응답자0명이다. LF 더미3항목 그림은 scripts/render-lf-fixture.py로 만들고 새 그림 검사3건 및 기존 산술7건을 통과했다. 상세는 research/03-results/lf-fixture-verification.md. 최종보고서v0.6의5·6절과 부록에 반영하고 PDF14쪽의 그림7쪽·참고문헌마지막 배치를 확인했다. 실제 우선순위·실증 분석·조사 실시 근거가 아니다.

## E-EVAL-001. 문항 검토·교수자 과업 패킷 준비

2026-10-27 저녁. [문항 검토 패킷](instrument-review-packet.md)의12행 빈 양식·4검토 관점과 research/03-results/faculty-task-protocol.md의8과업·R01–R12 대응을 작성했다. 실제 평정·전문가 검토·사용자 평가·기관 승인·CVI는 미실시/미확인이다. 보고서v0.7의10절·부록에 준비 사실만 반영했다.
