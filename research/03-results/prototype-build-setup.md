# 교수자용 소스 구조 정리와 배포 검증

## 작업 정보

- 작업일: 2026-10-23 (한국시간)
- 작업 목적: ZIP 안의 교수자용 소스를 직접 수정·실행·빌드·배포할 수 있는 프로젝트로 정리
- 제품 저장소: https://github.com/sam7614/TU-Professor-Assistant
- 제품 작업 브랜치: fix/professor-source-layout
- 소스 복원 커밋: 0da78a5
- 최종 운영 배포 커밋: fc31789011e90756fb38292959f225f757f5dd0d
- 선행 기록: [원본 코드 확인](prototype-source.md), [기존 대시보드 사전 검토](prototype-review.md)

## 코드 구조 변경

- ZIP의 교수자용 App, 데이터 상수, 타입 및 컴포넌트를 src에 복원했다.
- src/main.tsx를 진입점으로 지정하고 교수자용 index.html, Vite·TypeScript·Tailwind·PostCSS 설정을 정리했다.
- 기존 학생용·Streamlit 소스는 legacy/student-app에 보존하고 교수자용 빌드·배포에서 제외했다.
- 교수자용 의존성과 타입 정의를 선언하고 npm lockfile을 새로 생성했다.
- Tailwind 런타임 CDN과 import map 대신 정적 CSS·JS를 생성하는 로컬 빌드로 전환했다.
- 원본의 D3 타입 및 Recharts Cell 컴포넌트 오류를 수정했다.
- 모의 데이터임을 교수자 화면에 표시했다. 모의 데이터 자체를 실제 학사 데이터로 전환한 것은 아니다.
- 원본 ZIP과 환경 파일은 작업 로컬의 .local에 보관하고 현재 Git 트리에서 제외했다. 원본 출처는 이전 커밋과 docs/source-provenance.json으로 추적하며 Git 이력은 유지했다.

## 실행과 빌드 방법

- Node.js 22.12 이상 또는 24.x 사용
- 의존성 설치: npm ci
- 개발 실행: npm run dev (http://127.0.0.1:3000)
- 타입 검사: npm run typecheck
- 프로덕션 빌드: npm run build
- 산출물 확인: npm run preview
- 빌드 결과: dist
- 사용 안내: https://github.com/sam7614/TU-Professor-Assistant/blob/main/README.md
- 이관 근거: https://github.com/sam7614/TU-Professor-Assistant/blob/main/docs/MIGRATION.md

## 운영 프로젝트 연결 수정

기존 운영 프로젝트는 sam7614s-projects/micro-degree-student였고, 작업 전에는 별도 sam7614/micro-degree-student 저장소에 연결되어 있었다. 같은 Vercel 프로젝트와 도메인을 유지하면서 Git 연결을 sam7614/TU-Professor-Assistant의 main으로 변경했다. 이제 이 저장소 main의 변경이 기존 사이트의 자동 배포를 시작한다.

- 프로젝트 ID: prj_xPWOCmyJFvf7vaJtZrDgkiZWYfDB
- 운영 주소: https://micro-degree-student.vercel.app/
- 배포 ID: dpl_DxG5ibzxki7eMuo1aoucp3nCiYwt
- 고유 배포 URL: https://micro-degree-student-37d6o539d-sam7614s-projects.vercel.app
- 확인된 상태: READY / production
- 확인한 Git 메타데이터: repository=TU-Professor-Assistant, branch=main, commit=fc31789011e90756fb38292959f225f757f5dd0d
- 원격 빌드 시간: 약 22초

## 수행한 검증

- 새 lockfile의 npm ci 재설치 성공 (225 packages). 로컬 확인에서는 불필요한 설치 스크립트와 감사 요청을 생략했다.
- 엄격한 TypeScript 검사와 Vite 프로덕션 빌드 통과.
- 로컬 빌드 산출물과 실제 운영 주소에서 대시보드·학생 상세·학생 모듈 필터·개별 상담·D3 네트워크·모듈 통계·취업 사례 화면을 확인했다.
- 모바일 메뉴 이동 및 폭 390px에서 가로 넘침이 없음을 확인했다.
- 점검한 동선에서 JavaScript 예외 및 로컬/동일 사이트 빌드 자산의 404가 없었다.
- Vercel 배포의 저장소·브랜치·커밋·운영 도메인 메타데이터가 일치함을 확인했다.

## 해석과 남은 범위

이 작업은 초기 프로토타입의 개발·배포 기반을 정비한 기술 작업이다. 전문가 타당성 검증이나 교육적 효과 검증 결과로 사용하지 않는다. 상담 영속 저장, 실제 학사 데이터 연계, 학생 자기설계·성찰, 교수자 판단 이력 등은 별도 기능 개선 과제로 남아 있다.

단일 JavaScript 번들은 약 801 kB로 크기 경고가 있으므로 페이지별 코드 분리는 후속 성능 과제로 관리한다. 기존 모의 수치·무작위 데이터 및 일부 미연결 동작도 원본 상태임을 유지·구분한다.

## 연결 문서

- [프로토타입 본문](prototype.md)
- [근거 자료 목록](evidence.md)
- [남은 과제](tasks.md)
