# 교수자용 프로토타입 원본 코드 확인과 개발 방향

## 확인 정보

- 확인일: 2026-10-23 (한국시간)
- 연구자가 제시한 코드 저장소: https://github.com/sam7614/TU-Professor-Assistant
- 확인한 기본 브랜치: main
- 확인한 커밋: 74d467fb393906dbdc6ee76d898fada810dbb60a (Add files via upload)
- 배포 페이지: https://micro-degree-student.vercel.app/
- 비교 범위: 저장소 전체 파일 목록·기본 브랜치, ZIP 내부 소스, 공개 배포 HTML·클라이언트 번들, 해당 커밋의 GitHub Vercel 상태
- 확인 방식: GitHub 연결 도구 및 임시 읽기용 클론. 제품 저장소의 코드·설정·배포는 수정하지 않음.

## 판정

교수자용 대시보드와 대응하는 소스는 이 저장소의 tu-professor-assistant.zip 안에 들어 있다. 화면 제목·메뉴·상세 모달·모의 데이터·상담 가이드의 구체적 구현이 공개 배포본과 대응한다.

다만 저장소 최상위 소스는 ZIP 내부 프로젝트와 다르다. 따라서 저장소 주소를 찾았다는 사실과 현재 Vercel 사이트가 이 저장소의 main을 직접 자동 배포한다는 사실은 구분해야 한다. 배포 소스 커밋·Root Directory·도메인 연결은 아직 Vercel 프로젝트 설정에서 확인하지 않았다. 재현 빌드의 바이트 단위 일치는 검증하지 않았다.

## 저장소 구조에서 확인한 사실

### 최상위 코드

- App.tsx는 학습 이력, 모듈 탐색, 모듈 카트, 나의 모듈 설계, AI 추천으로 구성된 학생용 화면을 참조한다.
- 최상위 index.html의 제목은 TU 학습설계 AI 어시스턴트다.
- App.tsx가 참조하는 views 폴더는 확인한 커밋의 파일 목록에 없다. 현재 최상위 React 프로젝트는 필요한 소스가 누락된 상태로 보이며, 실제 빌드는 실행하지 않았다.
- app.py와 README_STREAMLIT.md도 학생용 학습설계 화면을 설명한다.

### ZIP 내부 코드

- App.tsx: TU 교수 지원, 대시보드·학생 관리·학습/진로 상담·메시지·모듈 분석 통계 메뉴 및 학생 상세 모달 연결.
- components/Dashboard.tsx: 지도학생과 이수율 등의 현황 화면, 고정 예시 수치 42·68 등.
- components/StudentManagement.tsx: 학생 관리 목록과 필터.
- components/ConsultationAdvisor.tsx: 개별 상담·클래스 네트워크, 진도율 조건에 따른 사전 코칭 문구.
- components/StudentModal.tsx: 학생 상세, 상담 브리핑·예시 이력·기록 입력창.
- components/PrintableReport.tsx: 상담 자료 출력용 구성.
- components/ModuleAnalytics.tsx 및 EmploymentModal.tsx: 모듈 통계와 취업 사례 모달.
- constants.ts: 모의 학생·평가·관계 데이터 생성과 공통 예시 상담 이력.
- index.html: 배포 페이지와 같은 TU 교수자용 학습설계 어시스턴트 제목.
- package.json: React·TypeScript·Vite 기반, lucide-react·Recharts·D3 사용.

## 배포본과의 대응 근거

- ZIP의 App.tsx와 공개 번들에 TU 교수 지원 화면 문구가 모두 존재한다.
- ZIP의 ConsultationAdvisor.tsx와 공개 번들에 진도율이 낮을 때 표시하는 동일한 코칭 문구가 존재한다.
- ZIP의 constants.ts와 공개 번들에 동일한 예시 상담 내용이 존재한다.
- ZIP의 StudentModal.tsx와 공개 번들에 동일한 상담 기록 입력 안내가 존재한다.
- 메뉴 구성과 교수자용 상세 화면의 구조도 앞선 화면 점검과 대응한다.

이 대응은 같은 교수자용 프로젝트 계열의 원본 소스를 식별하는 근거다. 수정되지 않은 동일 커밋이 운영 배포의 원본이라는 증명으로 확대하지 않는다.

## 확인 시점 식별값

- 배포 번들 URL: https://micro-degree-student.vercel.app/assets/index-BVt3XIGK.js
- 배포 번들 SHA-256: cea5c346629d20ee362f89eb2321ea6db49cdc1f3f8a22e13c1dd4277f224945
- 저장소 ZIP SHA-256: d991e48de88e5e97e75b2ff152d23db4c79a2892404156ab1f12ce449822e775
- ZIP 파일은 위 Git 커밋에 포함되어 있다. 공개 배포 번들은 영구 보관한 사본이 아니므로 재배포 후 같은 URL의 접근 가능성을 보장하지 않는다.

## GitHub의 Vercel 상태

확인한 커밋의 결합 상태에는 다음 두 검사가 failure로 표시되었다.

- Vercel: https://vercel.com/sam7614s-projects/tu-professor-assistant/CV4p6zcKDFeWWmbC2RjWH1LRw4ht
- Vercel – tu-professor-assistant-ktfa: https://vercel.com/sam7614s-projects/tu-professor-assistant-ktfa/9DWppXQEy7gcNYVNhAow64EdB7E4

빌드 로그를 확인하지 않았으므로 실패 원인을 단정하지 않는다. 이 상태가 현재 micro-degree-student.vercel.app의 운영 배포와 같은 프로젝트의 상태인지도 별도 확인이 필요하다.

## 향후 개발 방향 · 연구자 의사 반영

연구자는 현재 교수자용 페이지를 계속 개선하여 완성된 시스템으로 발전시키고자 한다. 기존 화면을 초기 버전으로 보관하고 기능·데이터·검증을 단계적으로 개선한다. 현재 연구기간의 최종 산출물 범위는 선정 계획서의 프로토타입 개발 및 타당성 검토를 기준으로 관리하며, 실제 운영 수준 고도화와 장기 효과 검증의 범위는 따로 명시한다.

### 1단계. 개발 기준 소스와 배포 경로 정리

- ZIP의 교수자용 코드를 일반 소스 파일 구조로 관리한다.
- 최상위 학생용·Streamlit 코드와 교수자용 프로젝트의 경계를 정한다. 기존 코드는 확인 없이 삭제·덮어쓰지 않는다.
- 개발 기준 커밋, 의존성 잠금 파일, 실행·빌드 절차와 환경 설정 항목을 정리한다.
- Vercel의 연결 저장소·브랜치·Root Directory·운영 도메인을 확인하고 검증 가능한 미리보기 배포를 만든다.
- 이 기록 시점에는 제품 저장소의 구조 변경이나 재배포를 수행하지 않았다.

### 2단계. 기존 기능의 실제 동작 완성

- 평가용 모의 데이터와 버전을 고정하고 요약 카드·목록·통계를 동일한 기준으로 집계한다.
- 페이지 전환, 검색, 상세 열기, 상담 일지와 메뉴 동선을 연결한다.
- 상담 기록의 학생별 저장·조회·수정·후속 조치를 완성한다.

### 3단계. 연구 핵심 기능과 검증

- 모듈 조합·설계 변경 이유·학생 성찰과 교수자 피드백을 연결한다.
- 시스템 제안의 입력 근거와 규칙/모델, 교수자 채택·수정·기각 이력을 추적한다.
- 문헌·요구 항목 → 설계 → 구현 → 평가 과업의 대응표를 유지한다.
- 전문가 검토·사용자 과업 평가와 필요 연구윤리 절차를 구체화하고 수행 결과를 보관한다.

## 연결 문서

- [기존 대시보드 사전 검토](prototype-review.md)
- [프로토타입 본문](prototype.md)
- [근거 자료 목록](evidence.md)
- [남은 과제](tasks.md)


## 후속 해결: 일반 소스 구조와 운영 Git 연결

같은 날 사용자 요청으로 ZIP의 교수자용 코드를 src로 복원하고 기존 학생용 소스를 legacy로 보존했다. 기존 운영 주소의 프로젝트가 다른 저장소에 연결되어 있음을 Vercel CLI에서 확인한 뒤, TU-Professor-Assistant/main으로 연결을 수정했다. 배포 커밋 fc31789011e90756fb38292959f225f757f5dd0d의 READY 상태와 주요 공개 화면을 확인했다. 위 확인 당시의 구조·연결 미확인 항목은 [소스 구조 정리와 배포 검증](prototype-build-setup.md)의 범위에서 해결되었다.
